from kit_up.core import exceptions as excs


class BaseUnitOfWorkExc(excs.BaseKitUpException):
    pass


class UowReEnterContextError(BaseUnitOfWorkExc):
    pass
