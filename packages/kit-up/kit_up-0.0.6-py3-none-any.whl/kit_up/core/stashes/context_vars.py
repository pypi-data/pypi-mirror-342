import collections
import contextvars
import typing as t

from kit_up.core.stashes import base

_DD = collections.defaultdict
_CONTEXTVARS: _DD[t.Any, t.Any] = _DD(dict)


class ContextVarStash(base.AbstractStash):
    def _stash_get(self, item):
        return _CONTEXTVARS[self][item].get()

    def _stash_set(self, key, value):
        store = _CONTEXTVARS[self]
        if key not in store:
            store[key] = contextvars.ContextVar(key)
        store[key].set(value)

    def _stash_del(self, item):
        del _CONTEXTVARS[self][item]
