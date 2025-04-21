from kit_up.core.units_of_work import base


class FdUow(base.BaseAbstractUnitOfWork):
    @property
    def _fd(self):
        return self._context.fd

    def open(self):
        return self._context.fd_open()

    def _begin(self):
        pass

    @property
    def active(self):
        return bool(self._fd)

    def flush(self):
        self._context.fd_flush()

    def commit(self) -> None:
        raise NotImplementedError

    def rollback(self) -> None:
        raise NotImplementedError

    def close(self) -> None:
        self._context.fd_close()
