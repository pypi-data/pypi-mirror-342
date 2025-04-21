import abc

from kit_up.core.contexts import base
from kit_up.core.mixins import require
from kit_up.core.units_of_work import exceptions as excs


class AbstractUnitOfWork(abc.ABC):  # Interface?
    @property
    @abc.abstractmethod
    def active(self):
        raise NotImplementedError

    @abc.abstractmethod
    def begin(self):  # TODO(d.burmistrov): open?
        raise NotImplementedError

    @abc.abstractmethod
    def commit(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def close(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def __enter__(self):
        raise NotImplementedError

    @abc.abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        raise NotImplementedError


class RequiresUnitOfWorkMixin(require.RequiresMixin, requires="uow"):
    _uow: AbstractUnitOfWork


class BaseAbstractUnitOfWork(
    AbstractUnitOfWork,
    base.RequiresContextMixin,
    abc.ABC,
):
    @abc.abstractmethod
    def _begin(self):
        raise NotImplementedError

    def begin(self):
        if self.active:
            raise excs.UowReEnterContextError()
        self._begin()
        return self

    def __enter__(self):
        return self.begin()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        handler = self.rollback if exc_type else self.commit
        try:
            handler()
        finally:
            self.close()
