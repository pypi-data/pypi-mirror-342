from kit_up.core.mixins import require


class AbstractContext:
    def __init__(self, **kwargs):
        pass


class RequiresContextMixin(require.RequiresMixin, requires="context"):
    _context: AbstractContext


class StashableContext(
    AbstractContext,
    require.RequiresMixin,
    requires="stash",
):
    def __init__(self, *, stash):
        self._stash = stash
