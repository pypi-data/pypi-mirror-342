import abc
import typing as t

from kit_up.core import models as mod_models
from kit_up.core.clauses import base as mod_clauses
from kit_up.core.mixins import crud, require
from kit_up.core.repositories import base
from kit_up.core.repositories import exceptions as repo_excs

# Sync


class AbstractSemiCrudRepository(
    base.AbstractRepository,
    crud.AbstractSemiCrud,
    abc.ABC,
):
    pass
    # TODO(d.burmistrov): functools.singledispatchmethod
    # @abc.abstractmethod
    # def destroy(self, identity_or_model) -> None:
    #     raise NotImplementedError


class _BaseRepository(require.RequiresMixin, requires="model_type"):
    _model_type: t.Type[mod_models.BaseModel]

    def get_model_type(self) -> type[mod_models.BaseModel]:
        return self._model_type

    def _to_storable(self, data: dict[str, t.Any]) -> t.Any:
        return data

    def _from_storable(self, storable: t.Any) -> dict[str, t.Any]:
        return storable.as_dict()

    def _storables_to_models(self, storables: t.Iterable[t.Any]):
        for item in storables:
            kwargs = self._from_storable(item)
            yield self._model_type(**kwargs)

    def _enrich_inputs(self, *inputs):
        for item in inputs:
            yield self._model_type.compute_defaults() | item


class RequiresCrudRepositoryMixin(base.RequiresRepositoryMixin):
    _repository: AbstractSemiCrudRepository


# TODO(d.burmistrov):
#   https://docs.python.org/3/library/functools.html#functools.singledispatchmethod
class AbstractBaseSemiCrudRepository(
    _BaseRepository,
    AbstractSemiCrudRepository,
    abc.ABC,
):

    # TODO(d.burmistrov): convert to generator?
    @abc.abstractmethod
    def _create(self, inputs: t.Iterable[dict[str, t.Any]]) -> t.Any:
        raise NotImplementedError

    # TODO(d.burmistrov): support sql/repo features
    # from kit_up.flavors.sql import base
    # def create(self, input, *inputs, _flavors: t.Iterable[base.SqlFlavor]
    #      ) -> tuple:
    def create(self, input, *inputs) -> tuple:
        data = self._enrich_inputs(input, *inputs)
        storables = self._create(data)
        models = tuple(self._storables_to_models(storables))
        return models

    def pick(self, identity):
        clause = self._model_type.make_identity_filter(identity)
        with repo_excs.EntityNotFoundExc.reraise():
            return self.get(clause)

    @abc.abstractmethod
    def _filter(self, *clauses: mod_clauses.BaseClause):
        raise NotImplementedError

    # TODO(d.burmistrov): rename to `def query(query_from_query_builder, ...)`?
    def filter(self, *clauses: mod_clauses.BaseClause) -> t.Iterable:
        storables = self._filter(*clauses)
        models = tuple(self._storables_to_models(storables))
        return models

    @abc.abstractmethod
    def update(self, model, *models) -> None:
        raise NotImplementedError

    def destroy(self, identity_or_model) -> None:
        clause = self._model_type.make_identity_filter(identity_or_model)
        return super().erase(clause)


# Async


class AbstractAsyncSemiCrudRepository(
    base.AbstractAsyncRepository,
    crud.AbstractAsyncSemiCrud,
    abc.ABC,
):
    pass


class RequiresAsyncCrudRepositoryMixin(base.RequiresRepositoryMixin):
    _repository: AbstractAsyncSemiCrudRepository


class AbstractBaseAsyncSemiCrudRepository(
    _BaseRepository,
    AbstractAsyncSemiCrudRepository,
    abc.ABC,
):
    @abc.abstractmethod
    async def _create(self, inputs) -> t.Any:
        raise NotImplementedError

    # TODO(d.burmistrov): support sql/repo features
    # from kit_up.flavors.sql import base
    # def create(self, input, *inputs, _flavors: t.Iterable[base.SqlFlavor]
    #      ) -> tuple:
    async def create(self, input, *inputs) -> tuple:
        data = self._enrich_inputs(input, *inputs)
        storables = await self._create(data)
        models = tuple(self._storables_to_models(storables))
        return models

    async def pick(self, identity):
        clause = self._model_type.make_identity_filter(identity)
        with repo_excs.EntityNotFoundExc.reraise():
            return await self.get(clause)

    @abc.abstractmethod
    async def _filter(self, *clauses: mod_clauses.BaseClause):
        raise NotImplementedError

    async def filter(self, *clauses: mod_clauses.BaseClause) -> t.Iterable:
        storables = await self._filter(*clauses)
        models = tuple(self._storables_to_models(storables))
        return models

    @abc.abstractmethod
    async def update(self, model, *models) -> None:
        raise NotImplementedError

    async def destroy(self, identity_or_model) -> int | None:
        clause = self._model_type.make_identity_filter(identity_or_model)
        return await super().erase(clause)
