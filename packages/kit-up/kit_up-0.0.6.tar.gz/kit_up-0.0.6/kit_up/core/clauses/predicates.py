import abc
import enum
import typing as t

from kit_up.core.clauses import base


class AbstractPredicateClause(base.BaseClause, abc.ABC):
    pass


class AbstractPredicateValueClause(AbstractPredicateClause):
    value: t.Any


class AbstractPredicateFieldClause(AbstractPredicateClause):
    field: str
    value: t.Any


class AbstractPredicateCompositeClause(AbstractPredicateValueClause):
    pass


# Field Predicates
class Eq(AbstractPredicateFieldClause):
    pass


class Ne(AbstractPredicateFieldClause):
    pass


class Gt(AbstractPredicateFieldClause):
    pass


class Ge(AbstractPredicateFieldClause):
    pass


class Lt(AbstractPredicateFieldClause):
    pass


class Le(AbstractPredicateFieldClause):
    pass


class Is(AbstractPredicateFieldClause):
    pass


class IsNot(AbstractPredicateFieldClause):
    pass


class In(AbstractPredicateFieldClause):
    pass


class NotIn(AbstractPredicateFieldClause):
    pass


# Composite Predicates
class ImplementedCompositeMixin:
    @classmethod
    def _from_parent(cls, parent: t.Any):
        if not isinstance(parent, ImplementedCompositeMixin):
            return super(ImplementedCompositeMixin, cls)._from_parent(parent)

        kls = cls.get_subclass_for(type(parent))

        if isinstance(parent.value, tuple):
            arg = tuple(
                super(ImplementedCompositeMixin, cls)._from_parent(item)
                for item in parent.value
            )
        else:
            arg = super(ImplementedCompositeMixin, cls)._from_parent(
                parent.value
            )

        return kls(arg)


class And(ImplementedCompositeMixin, AbstractPredicateCompositeClause):
    pass


class Or(ImplementedCompositeMixin, AbstractPredicateCompositeClause):
    pass


# Value Predicates
class Not(ImplementedCompositeMixin, AbstractPredicateCompositeClause):
    pass


# Helpers
class _BetweenFactory:
    class INCLUDE(enum.IntFlag):
        MIN = enum.auto()
        MAX = enum.auto()

        NONE = 0
        ALL = MIN | MAX

    def __init__(self, gt, ge, lt, le):
        self.gt = gt
        self.ge = ge
        self.lt = lt
        self.le = le

    def __call__(self, field: str, min, max, include: INCLUDE = INCLUDE.ALL):
        left = (self.gt, self.ge)[self.INCLUDE.MIN in include]
        right = (self.lt, self.le)[self.INCLUDE.MAX in include]
        return And((left(field, min), right(field, max)))


between = _BetweenFactory(Gt, Ge, Lt, Le)


def extract_predicate(*clauses):
    left, right = cells = ([], [])
    for cl in clauses:
        cells[isinstance(cl, AbstractPredicateClause)].append(cl)
    if len(right) > 1:
        right = And(tuple(right))
    elif right:
        right = right[0]
    else:
        right = None
    return tuple(left), right


def kv_to_predicate(**kwargs):
    result = extract_predicate(*(Eq(*item) for item in kwargs.items()))
    return tuple(item for item in result if item)
