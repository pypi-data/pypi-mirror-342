import abc
import typing as t

from kit_up.core.repositories import base


class AbstractExposableRepository(base.AbstractRepository, abc.ABC):
    @abc.abstractmethod
    def expose(self):
        raise NotImplementedError

    @abc.abstractmethod
    def execute(self, statement, *statements, **kwargs) -> t.Any | None:
        raise NotImplementedError


class AbstractExposableAsyncRepository(base.AbstractAsyncRepository, abc.ABC):
    @abc.abstractmethod
    async def expose(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def execute(self, statement, *statements, **kwargs) -> t.Any | None:
        raise NotImplementedError
