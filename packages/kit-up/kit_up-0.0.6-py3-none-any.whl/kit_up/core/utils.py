import typing as t


class EmptyResultExc(Exception):
    pass


class PluralResultExc(Exception):
    pass


def single_result(input: tuple, *, none_on_missing: bool = False):
    if len(input) > 1:
        raise PluralResultExc()
    elif input:
        return input[0]
    elif none_on_missing:
        return None
    else:
        raise EmptyResultExc()


def str_join(
    *items: t.Any,
    sep: str = ", ",
    str_func: t.Callable[[t.Any], str] = str,
) -> str:
    return sep.join(str_func(item) for item in items)
