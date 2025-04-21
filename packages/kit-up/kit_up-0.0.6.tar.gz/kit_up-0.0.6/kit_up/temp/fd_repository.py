from kit_up.core.contexts import base as ctx_base
from kit_up.core.repositories import base


class FdExposableRepositoryImpl(
    base.AbstractExposableRepository,
    ctx_base.RequiresContextMixin,
):
    def expose(self):
        return self._context.fd

    def execute(self, dat, *data) -> None:
        for d in (dat, *data):
            self._context.fd.write(d)
