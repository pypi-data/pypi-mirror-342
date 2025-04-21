import typing as t

from sqlalchemy import orm

from kit_up.core.contexts import base


class UowContextMixin(base.AbstractContext):
    uow: t.Any
    _session = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def uow_open(self):
        if self._session:
            raise Exception("УЖЕ ОТКРЫТО!!!")
        self._session = orm.Session(self.sa_engine)
        self._session.begin()

    @property
    def uow(self):
        if self._session is None:
            raise Exception("ЕЩЁ НЕТ ЕЁ!!!")
        return self._session

    def uow_close(self):
        if not self._session:
            raise Exception("УЖЕ ЗАКРЫТО!!!")
        self._session.close()
        self._session = None
