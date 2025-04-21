import collections
import os
import typing as t

import marshmallow as mm


def _filter(
    data: dict[str, str],
    prefix: str,
    key_normalizer: t.Callable[[str], str],
) -> t.Generator[tuple[str, str], None, None]:
    for key, value in data.items():
        key = key_normalizer(key)
        if key.startswith(prefix):
            yield key[len(prefix):], value


class EnvironNamespaced(collections.UserDict):
    def __init__(
        self,
        namespace: str,
        delimiter: str = "__",
        environ: os._Environ | dict[str, str] | None = None,
        prefix_normalizer: t.Callable[[str], str] = str.upper,
        environ_normalizer: t.Callable[[str], str] = str.upper,
    )  -> None:
        super().__init__()

        if environ is None:
            environ = os.environ

        self.data = dict(
            _filter(
                data=environ,
                prefix=prefix_normalizer(namespace + delimiter),
                key_normalizer=environ_normalizer,
            )
        )

        # prefix = prefix_normalizer(namespace + delimiter)
        # self.data = {
        #     k[len(prefix):]: v for k, v in environ.items()
        #     if k.startswith(prefix)
        # }


class EnvironGroup:
    def __init__(
        self,
        group_name: str | None,
        delimiter: str = "__",
        prefix_normalizer: t.Callable[[str], str] = str.upper,
        environ_normalizer: t.Callable[[str], str] = str.upper,
        post_normalizer: t.Callable[[str], str] = str.lower,
    ) -> None:
        self.group_name = group_name
        self.delimiter = delimiter
        self._prefix_normalizer = prefix_normalizer
        self._environ_normalizer = environ_normalizer
        self._post_normalizer = post_normalizer

    def __call__(
        self,
        data: os._Environ | dict[str, str] | None = None,
    ) -> dict[str, str]:
        if data is None:
            data = os.environ()

        if not data:
            return {}

        if self.group_name is None:
            return {key.lower(): value for key, value in data.items()}

        filtered = _filter(
            data=data,
            prefix=self._prefix_normalizer(self.group_name + self.delimiter),
            key_normalizer=self._environ_normalizer,
        )

        result = {self._post_normalizer(key): value for key, value in filtered}
        return result

        # prefix = self._prefix_normalizer(self.group_name + self.delimiter)
        # for key, value in data.items():
        #     key = self._environ_normalizer(key)
        #     if not key.startswith(prefix):
        #         continue
        #
        #     option = self._post_normalizer(key[len(prefix):])
        #     result[option] = value


class LoadEnvConfMixin:
    _Schema: t.ClassVar[t.Type[mm.Schema]]
    _Group: t.ClassVar[EnvironGroup]

    def __init_subclass__(cls, **kwargs) -> None:
        if not hasattr(cls, "_Schema"):
            cls._Schema = kwargs.pop("schema")
        if not hasattr(cls, "_Group"):
            cls._Group = kwargs.pop("group")
        cls._validate_fields()
        super().__init_subclass__(**kwargs)

    @classmethod
    def _validate_fields(cls):
        schema_fields = set(cls._Schema().declared_fields)
        dto_field = set(cls.__annotations__)
        aliens = schema_fields - dto_field
        if aliens:
            raise ValueError(f"Schema has fields out of dto: {list(aliens)}")

    @classmethod
    def from_env(
        cls,
        namespace: str | None = None,
        ns_delimiter: str = "__",
        environ: os._Environ | dict[str, str] | None = None,
    ) -> t.Self:
        if environ is None:
            data = os.environ

        if namespace is not None:
            data = EnvironNamespaced(
                namespace=namespace,
                delimiter=ns_delimiter,
            )

        schema = cls._Schema(partial=True, unknown=mm.EXCLUDE)
        data = cls._Group(data)
        data = schema.load(data)
        return cls(**data)
