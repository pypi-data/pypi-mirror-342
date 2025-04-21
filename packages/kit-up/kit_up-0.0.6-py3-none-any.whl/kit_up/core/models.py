import abc
import dataclasses
import functools
import types
import typing as t

import urnparse

from kit_up.core.clauses import predicates

RoDict = types.MappingProxyType

_KIT_UP = "kit-up"
_INITIALIZED = "_INITIALIZED"
_RO_DICT: RoDict = RoDict({})

_T_FACTORY = t.Callable[[], None]
_T_VALIDATOR = t.Callable[[t.Any], None]


# TODO(d.burmistrov): pickling
# TODO(d.burmistrov): .clone(**updates)


def _noop(*args, **kwargs):
    return


def field(
    *,
    private: bool = dataclasses.MISSING,  # type: ignore [assignment]
    validator: _T_VALIDATOR | None = None,
    **kwargs,
) -> dataclasses.Field:
    validator = validator or _noop
    meta = kwargs.setdefault("metadata", {})
    meta[_KIT_UP] = _FieldOpts(private=private, validator=validator)
    return dataclasses.field(**kwargs)


private_field = functools.partial(field, private=True)
public_field = functools.partial(field, private=False)
inner_field = public_field


class _FieldOpts(t.NamedTuple):
    private: bool
    validator: _T_VALIDATOR


_DEFAULT_FIELD_OPTS = field().metadata[_KIT_UP]


class AbstractEntity(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def get_identity_qualifier(cls):
        raise NotImplementedError

    @abc.abstractmethod
    def get_identity(self):
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def get_fields(cls) -> tuple[str, ...]:
        raise NotImplementedError

    @abc.abstractmethod
    def as_tuple(self) -> tuple[t.Any, ...]:
        raise NotImplementedError

    @abc.abstractmethod
    def as_dict(self) -> dict[str, t.Any]:
        raise NotImplementedError

    @abc.abstractmethod
    def copy(self) -> t.Self:
        raise NotImplementedError


class BaseModel(AbstractEntity):
    __privacy_policy__ = True
    __identity_qualifier__: str | tuple[str, ...] = "id"
    __publish_immutables__: str | tuple[str, ...] | None = None

    __INITIALIZED: bool = False

    __VIEW: t.ClassVar[type[AbstractEntity]]
    __DEFAULTS: t.ClassVar[
        tuple[
            RoDict[str, t.Any],
            tuple[tuple[str, _T_FACTORY], ...],
        ]
    ] = _RO_DICT, tuple()
    __PRIVATES: t.ClassVar[frozenset[str]] = frozenset()
    __VALIDATORS: t.ClassVar[RoDict[str, _T_VALIDATOR]] = _RO_DICT
    __PUBLIC_VIEW_API = (
        "__identity_qualifier__",
        "get_identity_qualifier",
        "get_identity",
        "get_fields",
        "as_tuple",
        "as_dict",
        "copy",
    )

    def __init_subclass__(cls) -> None:
        super(BaseModel, cls).__init_subclass__()
        dataclasses.dataclass(cls)

        validators = {}
        defaults = ({}, [])
        field_names, privates, occupied = set(), set(), set()
        for fld in dataclasses.fields(cls):
            cls.__preprocess_field(field_names, validators, fld)
            cls.__discover_default(fld, *defaults)
            cls.__discover_private(privates, occupied, fld)

        _name_conflict = field_names.intersection(occupied)
        if _name_conflict:
            msg = f"Private fields conflict with fields {_name_conflict}"
            raise AttributeError(msg)

        cls.__DEFAULTS = (RoDict(defaults[0]), tuple(defaults[1]))
        cls.__PRIVATES = frozenset(privates)
        cls.__VALIDATORS = RoDict(validators)

        # TODO(i.markevich): Maybe make some analog of Meta class
        #  for user defined view classes. And many more for think
        #  (abc, from_model, etc.)
        cls.__VIEW: type[AbstractEntity] = cls.__create_view()

    @classmethod
    def __preprocess_field(cls, field_names, validators, fld):
        field_names.add(fld.name)

        if _KIT_UP not in fld.metadata:
            meta = dict(fld.metadata) | {_KIT_UP: _DEFAULT_FIELD_OPTS}
            fld.metadata = RoDict(meta)

        validators[fld.name] = fld.metadata[_KIT_UP].validator

    @classmethod
    def __discover_default(cls, fld, static, factories):
        if fld.default is not dataclasses.MISSING:
            static[fld.name] = fld.default
        elif fld.default_factory is not dataclasses.MISSING:
            factories.append((fld.name, fld.default_factory))

    @classmethod
    def __discover_private(cls, privates, occupied, fld):
        private = fld.metadata[_KIT_UP].private
        if private is dataclasses.MISSING:
            private = cls.__privacy_policy__
        if not private:
            return
        if fld.name[1:2] == "_":
            msg = f"Private fields must be named publicly: {fld.name}"
            raise ValueError(msg)
        privates.add(fld.name)
        occupied.add(f"_{fld.name}")

    @classmethod
    def __create_view(cls) -> type[AbstractEntity]:
        ns = []
        ns_extra = cls.__publish_immutables__
        if isinstance(ns_extra, str):
            ns = [ns_extra]
        elif ns_extra:
            ns = ns_extra
        ns.extend(cls.__PUBLIC_VIEW_API)

        return dataclasses.make_dataclass(
            cls.__name__,
            ((fld.name, fld.type) for fld in dataclasses.fields(cls)),
            namespace={attr: getattr(cls, attr) for attr in ns},
            frozen=True,
            kw_only=True,
            slots=True,
#            module=cls.__module__,  # since 3.12
        )

    def _apply_validators(self):
        for fld, value in self.as_dict().items():
            self.__VALIDATORS[fld](value)

    def _validate(self):
        self._apply_validators()
        self.get_identity()

    def _setattr(self, key: str, value):
        if hasattr(self, key):
            self.__VALIDATORS[key](value)
        return super(BaseModel, self).__setattr__(key, value)

    def __setattr__(self, key: str, value):
        # Allow initialization during dataclass magic
        if not self.__INITIALIZED:
            return super(BaseModel, self).__setattr__(key, value)
        # Allow managing regular private attributes
        if key.startswith("_") and hasattr(self, key):
            return self._setattr(key, value)

        # Convert name for private field modification
        if key.startswith("_"):
            _key = key[1:]
            if _key in self.__PRIVATES:
                return self._setattr(_key, value)

        # Restrict private field modifications
        if key in self.__PRIVATES:
            msg = f"Forbidden to modify private attribute: {key}"
            raise AttributeError(msg)

        return self._setattr(key, value)

    def __delattr__(self, item):
        raise AttributeError("Attribute deletion is forbidden")

    @classmethod
    def get_fields(cls) -> tuple[str, ...]:
        return tuple(f.name for f in dataclasses.fields(cls))

    @classmethod
    def get_view_type(cls) -> type[AbstractEntity]:
        return cls.__VIEW

    @classmethod
    def compute_defaults(cls):
        if not cls.__DEFAULTS:
            return {}

        static, factories = cls.__DEFAULTS
        result = static.copy()
        result.update((fld_name, factory()) for fld_name, factory in factories)
        return result

    @classmethod
    def get_identity_qualifier(cls):
        return cls.__identity_qualifier__

    def get_identity(self):
        return getattr(self, self.get_identity_qualifier())

    def get_identity_filter(self):
        return self.make_identity_filter(self.get_identity())

    # @classmethod
    # def make_identity_filter(cls, identity):
    #     return predicates.Eq(cls.get_identity_qualifier(), identity)
    @classmethod
    def make_identity_filter(cls, identity_or_model):
        if isinstance(identity_or_model, cls):
            return identity_or_model.get_identity_filter()

        return predicates.Eq(cls.get_identity_qualifier(), identity_or_model)

    def as_view(self):
        return self.__VIEW(**self.as_dict())

    def as_urn(self) -> urnparse.URN8141:
        string = f"urn:model:{self.__class__.__name__}:{self.get_identity()}"
        return urnparse.URN8141.from_string(string)

    # Built-in serialization shortcuts
    as_tuple = dataclasses.astuple
    as_dict = dataclasses.asdict

    copy = dataclasses.replace
    clone = dataclasses.replace
