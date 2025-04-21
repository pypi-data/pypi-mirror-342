import abc


class AbstractStash(abc.ABC):
    @abc.abstractmethod
    def _stash_get(self, item):
        raise NotImplementedError

    @abc.abstractmethod
    def _stash_set(self, key, value):
        raise NotImplementedError

    @abc.abstractmethod
    def _stash_del(self, item):
        raise NotImplementedError


class AbstractAttrStash(AbstractStash, abc.ABC):
    def __getattr__(self, item):
        return self._stash_get(item)

    def __setattr__(self, key, value):
        return self._stash_set(key, value)

    def __delattr__(self, item):
        return self._stash_del(item)
