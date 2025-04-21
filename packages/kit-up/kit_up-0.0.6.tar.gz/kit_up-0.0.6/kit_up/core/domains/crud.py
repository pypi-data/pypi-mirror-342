import typing as t

from kit_up.core import models
from kit_up.core.clauses import base as bcls
from kit_up.core.clauses import predicates as dfs
from kit_up.core.domains import base
from kit_up.core.domains import exceptions as dom_excs
from kit_up.core.mixins import crud
from kit_up.core.repositories import crud as repos


class CrudDomain(
    base.AbstractDomain,
    crud.AbstractSemiCrud,
    repos.RequiresCrudRepositoryMixin,
):
    def get_view_type(self) -> type[models.AbstractEntity]:
        return self._repository.get_model_type().get_view_type()

    @dom_excs.UnexpectedExc.rewrap()
    def create(self, input, *inputs) -> tuple:
        with dom_excs.EntityConflictExc.reraise():
            data = self._repository.create(input, *inputs)
        return tuple(model.as_view() for model in data)

    @dom_excs.UnexpectedExc.rewrap()
    def pick(self, identity, *clauses: bcls.BaseClause):
        with dom_excs.EntityNotFoundExc.reraise():
            data = self._repository.pick(identity)
        return data.as_view()

    @dom_excs.UnexpectedExc.rewrap()
    def filter(self, *clauses: bcls.BaseClause) -> t.Iterable:
        data = self._repository.filter(*clauses)
        return tuple(item.as_view() for item in data)

    @dom_excs.UnexpectedExc.rewrap()
    def update(self, identity, updates) -> t.Any:
        # TODO(samuray21x): Re-write update for real correct updates :)
        with dom_excs.EntityNotFoundExc.reraise():
            model = self._repository.pick(identity)
        updated = model.clone(**updates)

        with dom_excs.EntityConflictExc.reraise():
            self._repository.update(updated)
        return updated.as_view()

    @dom_excs.UnexpectedExc.rewrap()
    def _erase(self, *filters: dfs.AbstractPredicateClause):
        return self._repository.erase(*filters)

    @dom_excs.UnexpectedExc.rewrap()
    def destroy(self, identity) -> None:
        with dom_excs.EntityNotFoundExc.reraise():
            return self._repository.destroy(identity)


class AsyncCrudDomain(
    base.AbstractAsyncDomain,
    crud.AbstractAsyncSemiCrud,
    repos.RequiresAsyncCrudRepositoryMixin,
):
    def get_view_type(self) -> type[models.AbstractEntity]:
        return self._repository.get_model_type().get_view_type()

    @dom_excs.UnexpectedExc.rewrap()
    async def create(self, input, *inputs) -> tuple:
        with dom_excs.EntityConflictExc.reraise():
            data = await self._repository.create(input, *inputs)
        return tuple(model.as_view() for model in data)

    @dom_excs.UnexpectedExc.rewrap()
    async def pick(self, identity, *clauses: bcls.BaseClause):
        with dom_excs.EntityNotFoundExc.reraise():
            data = await self._repository.pick(identity)
        return data.as_view()

    @dom_excs.UnexpectedExc.rewrap()
    async def filter(self, *clauses: bcls.BaseClause) -> t.Iterable:
        data = await self._repository.filter(*clauses)
        return tuple(item.as_view() for item in data)

    @dom_excs.UnexpectedExc.rewrap()
    async def update(self, identity, updates) -> t.Any:
        with dom_excs.EntityNotFoundExc.reraise():
            model = await self._repository.pick(identity)
        updated = model.clone(**updates)

        with dom_excs.EntityConflictExc.reraise():
            await self._repository.update(updated)
        return updated.as_view()

    @dom_excs.UnexpectedExc.rewrap()
    async def _erase(self, *filters: dfs.AbstractPredicateClause):
        return self._repository.erase(*filters)

    @dom_excs.UnexpectedExc.rewrap()
    async def destroy(self, identity) -> None:
        with dom_excs.EntityNotFoundExc.reraise():
            return await self._repository.destroy(identity)
