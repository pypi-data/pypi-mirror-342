import typing as t

from izulu import _reraise

from kit_up.core import exceptions as excs
from kit_up.core import utils
from kit_up.core.clauses import exceptions as cl_excs


class BaseRepositoryExc(excs.BaseKitUpException):
    pass


class EntityNotFoundExc(BaseRepositoryExc):
    __reraising__ = ((utils.EmptyResultExc, t.Self),)


class EntityConflictExc(BaseRepositoryExc):
    pass


class PluralResultExc(BaseRepositoryExc):
    pass


class ClauseRepositoryExc(BaseRepositoryExc, cl_excs.BaseClauseExc):
    pass


class UnknownClauseField(ClauseRepositoryExc, cl_excs.UnknownClauseField):
    pass


class UnsupportedClauseOperation(
    ClauseRepositoryExc,
    cl_excs.UnsupportedClauseOperation,
):
    pass


class UnprocessableClause(ClauseRepositoryExc, cl_excs.UnprocessableClause):
    pass


class UnexpectedExc(BaseRepositoryExc, _reraise.FatalMixin):
    __reraising__ = (
        # Pass all another repository exceptions
        (BaseRepositoryExc, None),
        # Handle and reraise any another exceptions
        (BaseException, t.Self),
        (Exception, t.Self),
    )
