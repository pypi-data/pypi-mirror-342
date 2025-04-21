import contextlib
import dataclasses
import typing as t


MISSING = object()


@dataclasses.dataclass(frozen=True)
class Require:
    attr_name: str
    private: bool = True
    kwarg_name: str = MISSING  # type: ignore[assignment]
    default: t.Any = MISSING
    default_factory: t.Callable[[], t.Any] = MISSING  # type: ignore

    def __post_init__(self):
        if self.default is not MISSING and self.default_factory is not MISSING:
            raise TypeError("Default factory and value can't be defined")
        if self.private and self.kwarg_name is not MISSING:
            raise TypeError("Private and kwarg_name can't be set together")
        if self.kwarg_name is MISSING:
            self.__dict__["kwarg_name"] = self.attr_name
        if self.private:
            self.__dict__["attr_name"] = "_" + self.attr_name

    def extract(self, kwargs: dict):
        value = kwargs.pop(self.kwarg_name, MISSING)
        if value is not MISSING:
            return self.attr_name, value
        elif self.default is not MISSING:
            return self.attr_name, self.default
        elif self.default_factory is not MISSING:
            return self.attr_name, self.default_factory()
        else:
            msg = f"Missing required keyword argument: '{self.kwarg_name}'"
            raise TypeError(msg) from None


class RequiresMixin:
    __REQUIRED_KWARGS: t.ClassVar[tuple[Require, ...]] = tuple()

    def __init_subclass__(cls, **kwargs) -> None:
        parents = []
        for kls in cls.__bases__:
            with contextlib.suppress(AttributeError):
                parents.extend(kls.__REQUIRED_KWARGS)
        cls.__REQUIRED_KWARGS = tuple(parents)

        required = kwargs.pop("requires", tuple())
        if required:
            if not isinstance(required, tuple):
                required = (required,)
            required = tuple(
                Require(attr_name=req) if isinstance(req, str) else req
                for req in required
            )
            cls.__REQUIRED_KWARGS += required

        super().__init_subclass__(**kwargs)

    def __init__(self, **kwargs):
        for requirement in self.__REQUIRED_KWARGS:
            attr_name, value = requirement.extract(kwargs)
            setattr(self, attr_name, value)
        super().__init__()
