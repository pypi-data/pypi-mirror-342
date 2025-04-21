from izulu import _reraise, root


class BaseKitUpException(root.Error, _reraise.ReraisingMixin):
    pass
