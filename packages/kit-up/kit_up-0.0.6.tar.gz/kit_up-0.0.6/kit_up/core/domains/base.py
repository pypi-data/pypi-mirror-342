from kit_up.core.mixins import require


class AbstractDomain:
    pass


class AbstractAsyncDomain:
    pass


class RequiresDomainMixin(require.RequiresMixin, requires="domain"):
    _domain: AbstractDomain


class RequiresAsyncDomainMixin(require.RequiresMixin, requires="domain"):
    _domain: AbstractAsyncDomain
