import operator

import sqlalchemy as sa

from kit_up.core.clauses import base
from kit_up.core.clauses import predicates


class BaseSqlalchemyFieldApplicator(
    predicates.ImplementedCompositeMixin,
    base.AbstractImplementedClauseMixin,
):
    __registry_type__ = "APPLICATORS_SQLALCHEMY_IMPL"

    def __call__(self):
        return self.OPERATOR(sa.column(self.field), self.value)


class Eq(BaseSqlalchemyFieldApplicator, predicates.Eq):
    OPERATOR = operator.eq


class Ne(BaseSqlalchemyFieldApplicator, predicates.Ne):
    OPERATOR = operator.ne


class Gt(BaseSqlalchemyFieldApplicator, predicates.Gt):
    OPERATOR = operator.gt


class Ge(BaseSqlalchemyFieldApplicator, predicates.Ge):
    OPERATOR = operator.ge


class Lt(BaseSqlalchemyFieldApplicator, predicates.Lt):
    OPERATOR = operator.lt


class Le(BaseSqlalchemyFieldApplicator, predicates.Le):
    OPERATOR = operator.le


class Is(BaseSqlalchemyFieldApplicator, predicates.Is):
    OPERATOR = operator.is_


class IsNot(BaseSqlalchemyFieldApplicator, predicates.IsNot):
    OPERATOR = operator.is_not


class In(BaseSqlalchemyFieldApplicator, predicates.In):
    OPERATOR = operator.contains


class NotIn(BaseSqlalchemyFieldApplicator, predicates.NotIn):
    OPERATOR = lambda a, b: a not in b  # noqa


class And(BaseSqlalchemyFieldApplicator, predicates.And):
    def __call__(self):
        return sa.and_(item() for item in self.value)


class Or(BaseSqlalchemyFieldApplicator, predicates.Or):
    def __call__(self):
        return sa.or_(item() for item in self.value)


class Not(BaseSqlalchemyFieldApplicator, predicates.Not):
    def __call__(self):
        return sa.not_(self.value[0]())
