import abc
import operator

from kit_up.core.clauses import base
from kit_up.core.clauses import predicates


def _not_contains(a, b, /):
    return b not in a


class AbstractApplicator(
    base.BaseClause,
    base.AbstractImplementedClauseMixin,
    abc.ABC,
):
    __registry_type__ = "APPLICATORS"


class _PredicateFieldApplicator(AbstractApplicator, abc.ABC):
    @classmethod
    def OPERATOR(cls, *args, **kwargs):
        raise NotImplementedError

    def __call__(self, model):
        return self.OPERATOR(self.value, getattr(model, self.field))


# Field Predicates
class Eq(_PredicateFieldApplicator, predicates.Eq, AbstractApplicator):
    OPERATOR = operator.eq


class Ne(_PredicateFieldApplicator, predicates.Ne, AbstractApplicator):
    OPERATOR = operator.ne


class Gt(_PredicateFieldApplicator, predicates.Gt, AbstractApplicator):
    OPERATOR = operator.gt


class Ge(_PredicateFieldApplicator, predicates.Ge, AbstractApplicator):
    OPERATOR = operator.ge


class Lt(_PredicateFieldApplicator, predicates.Lt, AbstractApplicator):
    OPERATOR = operator.lt


class Le(_PredicateFieldApplicator, predicates.Le, AbstractApplicator):
    OPERATOR = operator.le


class Is(_PredicateFieldApplicator, predicates.Is, AbstractApplicator):
    OPERATOR = operator.is_


class IsNot(_PredicateFieldApplicator, predicates.IsNot, AbstractApplicator):
    OPERATOR = operator.is_not


class In(_PredicateFieldApplicator, predicates.In, AbstractApplicator):
    OPERATOR = operator.contains


class NotIn(_PredicateFieldApplicator, predicates.NotIn, AbstractApplicator):
    OPERATOR = _not_contains


# Composite Predicate
class And(predicates.And, AbstractApplicator):
    def __call__(self):
        return all(item() for item in self.value)


class Or(predicates.Or, AbstractApplicator):
    def __call__(self):
        return any(item() for item in self.value)


# Value Predicates
class Not(predicates.Not, AbstractApplicator):
    def __call__(self):
        return not self.value[0]()


between = predicates._BetweenFactory(Gt, Ge, Lt, Le)
