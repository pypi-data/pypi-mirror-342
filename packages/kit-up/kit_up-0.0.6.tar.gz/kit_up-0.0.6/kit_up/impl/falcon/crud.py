import abc
import typing as t

import falcon

from kit_up.core import models
from kit_up.core.clauses import predicates
from kit_up.core.domains import base as dom_base
from kit_up.core.domains import exceptions as dom_excs
from kit_up.impl.falcon import errors

_CODES = falcon.status_codes


def to_clauses(params, *, key_name: str | None = None):
    if key_name:
        key = params[key_name]
        return (predicates.Eq(key_name, key),)
    # TODO(i.markevich): Add clauses for params good work with
    #  requests like name=john&surname=Some
    return tuple()


class AbstractCrudController:
    @abc.abstractmethod
    def on_get(self, req: falcon.Request, resp: falcon.Response, **path_fields):
        raise NotImplementedError

    @abc.abstractmethod
    def on_patch(self, req: falcon.Request, resp: falcon.Response, **path_fields):
        raise NotImplementedError

    @abc.abstractmethod
    def on_put(self, req: falcon.Request, resp: falcon.Response, **path_fields):
        raise NotImplementedError

    @abc.abstractmethod
    def on_delete(self, req: falcon.Request, resp: falcon.Response, **path_fields):
        raise NotImplementedError

    @abc.abstractmethod
    def on_get_collection(self, req: falcon.Request, resp: falcon.Response):
        raise NotImplementedError

    @abc.abstractmethod
    def on_post_collection(self, req: falcon.Request, resp: falcon.Response):
        raise NotImplementedError


class AbstractAsyncCrudController:
    @abc.abstractmethod
    async def on_get(self, req: falcon.Request, resp: falcon.Response, **path_fields):
        raise NotImplementedError

    @abc.abstractmethod
    async def on_patch(self, req: falcon.Request, resp: falcon.Response, **path_fields):
        raise NotImplementedError

    @abc.abstractmethod
    async def on_put(self, req: falcon.Request, resp: falcon.Response, **path_fields):
        raise NotImplementedError

    @abc.abstractmethod
    async def on_delete(
        self,
        req: falcon.Request,
        resp: falcon.Response,
        **path_fields,
    ):
        raise NotImplementedError

    @abc.abstractmethod
    async def on_get_collection(self, req: falcon.Request, resp: falcon.Response):
        raise NotImplementedError

    @abc.abstractmethod  # 201 + Location
    async def on_post_collection(self, req: falcon.Request, resp: falcon.Response):
        raise NotImplementedError


class BaseCrudController(dom_base.RequiresDomainMixin):
    # TODO(i.markevich): provide base media handler for models (actually views).
    #  Maybe derive view from dict/UserDict and provide such interface
    #  for native convertion
    @property
    def view_type(self) -> type[models.AbstractEntity]:
        return self._domain.get_view_type()

    @property
    def identity_qualifier(self):
        return self.view_type.get_identity_qualifier()

    def _extract_identity(self, path_fields: dict[str, t.Any]) -> t.Any:
        qualifier = self.identity_qualifier
        try:
            return path_fields[qualifier]
        except KeyError as e:
            err_msg = f'Identity qualifier "{qualifier}" not found in path params'
            raise errors.BadRequestError(description=err_msg) from e

    def _validate_update_request_by_view(self, req: falcon.Request) -> None:
        """
        Validate update request param, like body,
        for correlation with domain view.
        """
        # TODO(i.markevich): Exclude or not identity qualifier
        #  from body fields check https://stackoverflow.com/a/60535208
        expected_fields = set(self.view_type.get_fields())
        actual_fields = set(req.media)

        if actual_fields != expected_fields:
            err_desc = ""
            if missed_fields := expected_fields - actual_fields:
                err_desc = f"Missed fields: {','.join(sorted(missed_fields))}"

            if extra_fields := actual_fields - expected_fields:
                if err_desc:
                    err_desc += " | "
                err_desc += f"Undefined fields: {','.join(sorted(extra_fields))}"

            raise errors.BadRequestError(description=err_desc)

    def _raise_not_found(self, identity: t.Any):
        dsc = f"Entry with identity {self.identity_qualifier}={identity} not found"
        raise errors.NotFoundError(description=dsc)


class CrudController(BaseCrudController, AbstractCrudController):
    def _pick(self, identity: t.Any) -> models.AbstractEntity:
        try:
            return self._domain.pick(identity)
        except dom_excs.EntityNotFoundExc:
            self._raise_not_found(identity)

    def on_get(self, req: falcon.Request, resp: falcon.Response, **path_fields):
        if req.params:
            view = self._domain.get(
                to_clauses(req.params, key_name=self.identity_qualifier)
            )
        else:
            view = self._pick(self._extract_identity(path_fields))
        resp.media = view.as_dict()
        resp.status_code = _CODES.HTTP_OK

    def on_patch(self, req: falcon.Request, resp: falcon.Response, **path_fields):
        """Partial resource rewrite (subset of fields)."""
        identity = self._extract_identity(path_fields)

        if req.media:
            try:
                self._domain.update_by(identity, **req.media)
            except dom_excs.EntityNotFoundExc:
                self._raise_not_found(identity)

        resp.media = self._pick(identity).as_dict()

    def on_put(self, req: falcon.Request, resp: falcon.Response, **path_fields):
        """Complete resource rewrite (full set of fields)."""
        identity = self._extract_identity(path_fields)
        self._validate_update_request_by_view(req)

        try:
            self._domain.update_by(identity, **req.media)
        except dom_excs.EntityNotFoundExc:
            self._raise_not_found(identity)

        # EntityNotFoundExc is not expected here
        resp.media = self._pick(identity).as_dict()

    def on_delete(self, req: falcon.Request, resp: falcon.Response, **path_fields):
        identity = self._extract_identity(path_fields)
        try:
            self._domain.destroy(identity)
        except dom_excs.EntityNotFoundExc:
            self._raise_not_found(identity)
        resp.status_code = _CODES.HTTP_NO_CONTENT

    def on_get_collection(self, req: falcon.Request, resp: falcon.Response):
        views = self._domain.filter(to_clauses(req.params))
        resp.media = [view.as_dict() for view in views]

    # 201 + Location
    def on_post_collection(self, req: falcon.Request, resp: falcon.Response):
        try:
            view = self._domain.create(req.media)[0]
        except dom_excs.EntityConflictExc as e:
            dsc = "Entry conflict with exists one"
            raise errors.DuplicateEntryError(description=dsc) from e

        resp.media = view.as_dict()
        resp.status_code = _CODES.HTTP_OK


class AsyncCrudController(BaseCrudController, AbstractAsyncCrudController):
    async def _pick(self, identity: t.Any) -> models.AbstractEntity:
        try:
            return await self._domain.pick(identity)
        except dom_excs.EntityNotFoundExc:
            self._raise_not_found(identity)

    async def on_get(self, req: falcon.Request, resp: falcon.Response, **path_fields):
        if req.params:
            view = await self._domain.get(
                to_clauses(req.params, key_name=self.identity_qualifier)
            )
        else:
            view = await self._pick(self._extract_identity(path_fields))
        resp.media = view.as_dict()
        resp.status_code = _CODES.HTTP_OK

    async def on_patch(self, req: falcon.Request, resp: falcon.Response, **path_fields):
        """Partial resource rewrite (subset of fields)."""
        identity = self._extract_identity(path_fields)

        if req.media:
            try:
                await self._domain.update_by(identity, **req.media)
            except dom_excs.EntityNotFoundExc:
                self._raise_not_found(identity)

        # EntityNotFoundExc is not expected here
        view = await self._pick(identity)
        resp.media = view.as_dict()

    async def on_put(self, req: falcon.Request, resp: falcon.Response, **path_fields):
        """Complete resource rewrite (full set of fields)."""
        identity = self._extract_identity(path_fields)
        self._validate_update_request_by_view(req)

        try:
            await self._domain.update_by(identity, **req.media)
        except dom_excs.EntityNotFoundExc:
            self._raise_not_found(identity)

        # EntityNotFoundExc is not expected here
        view = await self._pick(identity)
        resp.media = view.as_dict()

    async def on_delete(
        self,
        req: falcon.Request,
        resp: falcon.Response,
        **path_fields,
    ):
        identity = self._extract_identity(path_fields)
        try:
            await self._domain.destroy(identity)
        except dom_excs.EntityNotFoundExc:
            self._raise_not_found(identity)
        resp.status_code = _CODES.HTTP_NO_CONTENT

    async def on_get_collection(self, req: falcon.Request, resp: falcon.Response):
        views = await self._domain.filter(to_clauses(req.params))
        resp.media = [view.as_dict() for view in views]

    async def on_post_collection(self, req: falcon.Request, resp: falcon.Response):
        try:
            view = await self._domain.create(req.media)[0]
        except dom_excs.EntityConflictExc as e:
            dsc = "Entry conflict with exists one"
            raise errors.DuplicateEntryError(description=dsc) from e

        resp.media = view.as_dict()
        resp.status_code = _CODES.HTTP_OK


def _rstrip_slash(string: str) -> str:
    return string.rstrip("/")


class AddCrudRouteMixin:
    def add_crud_route(
        self,
        base_uri: str,
        ctrl: BaseCrudController,
        /,
        **kwargs: t.Any,
    ) -> None:
        """
        Connect routes for CRUD controller.

        Auto-append domain model identity qualifier to base_uri.
        """
        path_identity_qualifier = ctrl.identity_qualifier
        path_spec = _rstrip_slash(base_uri)

        # Valid: /items | /items/
        # Not valid: /items/{name} | /items/{name}/
        if path_spec[-1] == "}":
            # TODO(i.markevich): good error
            raise ValueError("")
            # path_spec, path_spec_qualifier = path_spec[:-1].split("{", maxsplit=1)
            # path_spec = _rstrip_slash(path_spec)
            # if path_spec_qualifier and path_spec_qualifier != path_identity_qualifier:
            #     # TODO(i.markevich): good error
            #     error = (f"Wrong path specification, "
            #              f"expected path qualifier: {path_identity_qualifier}, "
            #              f"got {path_spec_qualifier}")
            #     raise ValueError(error)

        self.add_route(f"{path_spec}/{{{path_identity_qualifier}}}", ctrl, **kwargs)
        self.add_route(path_spec, ctrl, suffix="collection", **kwargs)
