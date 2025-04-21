from kit_up.core.contexts import base


class FdContextMixin(base.StashableContext):
    def __init__(self, *, path: str, **kwargs):
        super().__init__(**kwargs)
        self.path = path
        self._fd = None

    @property
    def fd(self):
        return self._fd

    def fd_open(self, mode="w", buffering=1):
        if self._fd:
            raise RuntimeError("AlreadyOpen")
        self._fd = open(self.path, mode=mode, buffering=buffering)
        return self._fd

    def fd_flush(self):
        self._fd.flush()

    def fd_close(self):
        self._fd.close()
        self._fd = None
