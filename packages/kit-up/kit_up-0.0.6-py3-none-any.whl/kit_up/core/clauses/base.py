import abc
import dataclasses
import typing as t

from miska import registries as rr


# TODO(d.burmistrov): cache?
def resolve_clause_type(klass: t.Any):
    for kls in getattr(klass, "__mro__", tuple()) + (klass,):
        is_implementation = getattr(kls, "__is_implementation__", False)
        if issubclass(kls, BaseClause) and is_implementation is False:
            return kls
    return None


# TODO(d.burmistrov): dataclasses + init_subclass wrap (like model)
class BaseClause:
    def __init_subclass__(cls) -> None:
        super(BaseClause, cls).__init_subclass__()
        dataclasses.dataclass(cls)

    def as_tuple(self):
        return dataclasses.astuple(self)

    def as_dict(self):
        return dataclasses.asdict(self)


# TODO(d.burmistrov): Implemented --> Applicable??
class AbstractImplementedClauseMixin(rr.ClassRegistriesMixin, abc.ABC):
    __is_implementation__: bool = True
    __registry_qualifier__ = resolve_clause_type

    @classmethod
    def get_subclass_for(cls, identity: t.Type[BaseClause]) -> type:
        return super().get_subclass_for(resolve_clause_type(identity))

    @classmethod
    def _from_parent(cls, parent: t.Any):
        kls = cls.get_subclass_for(type(parent))
        obj = kls(**parent.as_dict())
        return obj

    @classmethod
    def from_parent(cls, parent: t.Any):
        return cls._from_parent(parent)

    @abc.abstractmethod
    def __call__(self, *args, **kwargs):
        raise NotImplementedError
