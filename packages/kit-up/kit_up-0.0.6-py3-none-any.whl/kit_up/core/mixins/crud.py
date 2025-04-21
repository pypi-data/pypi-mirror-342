import abc
import typing as t

from kit_up.core import utils
from kit_up.core.clauses import base as bfs
from kit_up.core.clauses import predicates as dfs


def _validate_erase_args(clauses, force):
    if not clauses and not force:
        raise ValueError  # TODO(d.burmistrov): normal exceptions


# Sync

class AbstractCrud(abc.ABC):
    @abc.abstractmethod
    def create(self, input, *inputs) -> tuple:
        raise NotImplementedError

    @abc.abstractmethod
    def create_by(self, **paired) -> t.Any:
        raise NotImplementedError

    @abc.abstractmethod
    def pick(self, identity, *clauses: bfs.BaseClause) -> t.Any:
        raise NotImplementedError

    @t.overload
    def get(
        self,
        filter: dfs.AbstractPredicateClause,
        *clauses: bfs.BaseClause,
        _or_none: t.Literal[False],
    ) -> t.Any:
        raise NotImplementedError

    @t.overload
    def get(
        self,
        filter: dfs.AbstractPredicateClause,
        *clauses: bfs.BaseClause,
        _or_none: t.Literal[True],
    ) -> t.Any | None:
        raise NotImplementedError

    @abc.abstractmethod
    def get(
        self,
        filter: dfs.AbstractPredicateClause,
        *clauses: bfs.BaseClause,
        _or_none: bool = False,
    ) -> t.Any | None:
        raise NotImplementedError

    @t.overload
    def get_by(self, *, _or_none: t.Literal[False], **kvs) -> t.Any:
        raise NotImplementedError

    @t.overload
    def get_by(self, *, _or_none: t.Literal[True], **kvs) -> t.Any | None:
        raise NotImplementedError

    @abc.abstractmethod
    def get_by(self, *, _or_none: bool = False, **kvs) -> t.Any | None:
        raise NotImplementedError

    @abc.abstractmethod
    def filter(
        self,
        *clauses: bfs.BaseClause,
        _limit=None,
        _marker=None,
        _order_by=...,
    ) -> t.Iterable:
        raise NotImplementedError

    # *clauses: bfs.BaseClause,
    # _for_update
    @abc.abstractmethod
    def filter_by(self, **kvs) -> t.Iterable:
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, *args, **kwargs) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def update_by(self, identity, **kvs):
        raise NotImplementedError

    @abc.abstractmethod
    def destroy(self, identity) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def erase(
        self,
        *filters: dfs.AbstractPredicateClause,
        _force: bool = False,
        # limit? which clauses?
    ) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def erase_by(self, **paired) -> int:
        raise NotImplementedError


class AbstractSemiCrud(AbstractCrud, abc.ABC):
    def create_by(self, **paired) -> t.Any:
        created = self.create(paired)
        return created[0]

    def get(
        self,
        filter: dfs.AbstractPredicateClause,
        *clauses: bfs.BaseClause,
        _or_none: bool = False,
    ) -> t.Any | None:
        # TODO(d.burmistrov): ensure (Limit=2)
        result = tuple(self.filter(filter, *clauses))
        result = utils.single_result(result)
        return result

    def get_by(self, **kvs) -> t.Any | None:
        return self.get(*dfs.kv_to_predicate(**kvs))

    def filter_by(self, **kvs) -> t.Iterable[t.Any]:
        clauses = dfs.kv_to_predicate(**kvs)
        return self.filter(*clauses)

    def update_by(self, identity, **kvs):
        return self.update(identity, kvs)

    @abc.abstractmethod
    def _erase(self, *filters: dfs.AbstractPredicateClause) -> t.Any:
        raise NotImplementedError

    def erase(
        self,
        *filters: dfs.AbstractPredicateClause,
        _force: bool = False,
    ) -> int:
        _validate_erase_args(filters, _force)
        return self._erase(*filters)

    def erase_by(self, **kvs) -> int:
        return self.erase(*dfs.kv_to_predicate(**kvs))


# Async

class AbstractAsyncCrud(abc.ABC):
    @abc.abstractmethod
    async def create(self, input, *inputs) -> tuple:
        raise NotImplementedError

    @abc.abstractmethod
    async def create_by(self, **paired) -> t.Any:
        raise NotImplementedError

    @abc.abstractmethod
    async def pick(self, identity, *clauses: bfs.BaseClause) -> t.Any:
        raise NotImplementedError

    @t.overload
    async def get(
        self,
        filter: dfs.AbstractPredicateClause,
        *clauses: bfs.BaseClause,
        _or_none: t.Literal[False],
    ) -> t.Any:
        raise NotImplementedError

    @t.overload
    async def get(
        self,
        filter: dfs.AbstractPredicateClause,
        *clauses: bfs.BaseClause,
        _or_none: t.Literal[True],
    ) -> t.Any | None:
        raise NotImplementedError

    @abc.abstractmethod
    async def get(
        self,
        filter: dfs.AbstractPredicateClause,
        *clauses: bfs.BaseClause,
        _or_none: bool = False,
    ) -> t.Any | None:
        raise NotImplementedError

    @t.overload
    async def get_by(self, *, _or_none: t.Literal[False], **kvs) -> t.Any:
        raise NotImplementedError

    @t.overload
    async def get_by(self, *, _or_none: t.Literal[True], **kvs) -> t.Any | None:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_by(self, *, _or_none: bool = False, **kvs) -> t.Any | None:
        raise NotImplementedError

    @abc.abstractmethod
    async def filter(
        self,
        *clauses: bfs.BaseClause,
        _limit=None,
        _marker=None,
        _order_by=...,
    ) -> t.Iterable:
        raise NotImplementedError

    # *clauses: bfs.BaseClause,
    # _for_update
    @abc.abstractmethod
    async def filter_by(self, **kvs) -> t.Iterable:
        raise NotImplementedError

    @abc.abstractmethod
    async def update(self, *args, **kwargs) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def update_by(self, identity, **kvs):
        raise NotImplementedError

    @abc.abstractmethod
    async def destroy(self, identity) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def erase(
        self,
        *filters: dfs.AbstractPredicateClause,
        _force: bool = False,
        # limit? which clauses?
    ) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    async def erase_by(self, **paired) -> int:
        raise NotImplementedError


class AbstractAsyncSemiCrud(AbstractAsyncCrud, abc.ABC):
    async def create_by(self, **paired) -> t.Any:
        created = await self.create(paired)
        return created[0]

    async def get(
        self,
        filter: dfs.AbstractPredicateClause,
        *clauses: bfs.BaseClause,
        _or_none: bool = False,
    ) -> t.Any | None:
        # TODO(d.burmistrov): ensure (Limit=2)
        result = tuple(await self.filter(filter, *clauses))
        result = utils.single_result(result)
        return result

    async def get_by(self, **kvs) -> t.Any | None:
        return await self.get(*dfs.kv_to_predicate(**kvs))

    async def filter_by(self, **kvs) -> t.Iterable[t.Any]:
        return await self.filter(*dfs.kv_to_predicate(**kvs))

    async def update_by(self, identity, **kvs):
        return await self.update(identity, kvs)

    @abc.abstractmethod
    async def _erase(self, *filters: dfs.AbstractPredicateClause) -> t.Any:
        raise NotImplementedError

    async def erase(
        self,
        *filters: dfs.AbstractPredicateClause,
        _force: bool = False,
    ) -> int:
        _validate_erase_args(filters, _force)
        return await self._erase(*filters)

    async def erase_by(self, **kvs) -> int:
        return await self.erase(*dfs.kv_to_predicate(**kvs))
