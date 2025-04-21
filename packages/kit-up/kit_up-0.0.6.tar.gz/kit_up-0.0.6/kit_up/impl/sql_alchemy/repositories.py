import typing as t

import sqlalchemy as sa

from kit_up.core.clauses import base as bfs
from kit_up.core.clauses import predicates as dfs
from kit_up.core.contexts.base import RequiresContextMixin
from kit_up.core.repositories import exposable
from kit_up.core.repositories import crud
from kit_up.impl.sql_alchemy import applicators as sa_fltrs
from kit_up.impl.sql_alchemy import require


def _apply_filter(stmt, filter):
    if not filter:
        return stmt

    filter = sa_fltrs.BaseSqlalchemyFieldApplicator.from_parent(filter)
    return stmt.where(filter())


class SqlalchemyExposableRepository(
    exposable.AbstractExposableRepository,
    require.RequiresSqlalchemySessionMixin,
):
    def expose(self):
        return self._context.uow

    def execute(self, statement, *args, **kwargs) -> t.Any | None:
        return self._context.uow.execute(statement, *args, **kwargs)


class SqlalchemyCrudRepository(
    crud.AbstractBaseSemiCrudRepository,
    RequiresContextMixin,  # RequiresUowContextMixin
    requires="orm_type",
):
    def _to_storable(self, data: dict[str, t.Any]) -> t.Any:
        return self._orm_type(**data)

    def _create(self, inputs):
        data = tuple(self._to_storable(item) for item in inputs)
        self._context.uow.add_all(data)
        self._context.uow.flush(data)
        return data

    def _filter(self, *clauses: bfs.BaseClause):
        clauses, filter = dfs.extract_predicate(*clauses)
        stmt = sa.select(self._orm_type)
        stmt = _apply_filter(stmt, filter)
        return self._context.uow.scalars(stmt)

    def update(self, model, *models) -> None:
        merged = []
        for m in (model, *models):
            merged.append(self._context.uow.merge(m.as_dict()))
        self._context.uow.flush(merged)

    def _erase(self, *filters: dfs.AbstractPredicateClause):
        clauses, filter = dfs.extract_predicate(*filters)
        stmt = sa.delete(self._orm_type)
        stmt = _apply_filter(stmt, filter)
        return self._context.uow.scalars(stmt)

    # def destroy(self, identity_or_model) -> None:
    #     if isinstance(identity_or_model, self._data_mapper.model_type):
    #         self._context.uow.delete(identity_or_model)
    #     else:
    #         super().destroy(identity_or_model)
