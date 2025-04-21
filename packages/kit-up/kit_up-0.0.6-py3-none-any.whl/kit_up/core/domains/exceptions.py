import typing as t

from izulu import _reraise

from kit_up.core import exceptions as excs
from kit_up.core.repositories import exceptions as repo_excs


class BaseDomainExc(excs.BaseKitUpException):
    pass


class EntityNotFoundExc(BaseDomainExc):
    __reraising__ = ((repo_excs.EntityNotFoundExc, t.Self),)


class EntityConflictExc(BaseDomainExc):
    __reraising__ = ((repo_excs.EntityConflictExc, t.Self),)


class PluralResultExc(BaseDomainExc):
    __reraising__ = ((repo_excs.PluralResultExc, t.Self),)


class UnexpectedExc(BaseDomainExc, _reraise.FatalMixin):
    __reraising__ = (
        # Pass all another domain exceptions
        (BaseDomainExc, None),
        # Handle and reraise any another exceptions
        (BaseException, t.Self),
        (Exception, t.Self),
    )
