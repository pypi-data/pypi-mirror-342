import typing as t

from izulu import root

from kit_up.core.clauses import base as bcs


class BaseClauseExc(root.Error):
    __template__: t.ClassVar[str] = "Clause error for {clause}"
    clause: bcs.BaseClause


class UnknownClauseField(BaseClauseExc):
    __template__: t.ClassVar[str] = "Clause field {unknown_field} is unknown"
    unknown_field: str = root.factory(
        default_factory=lambda self: self.clause.field,
        self=True,
    )


class UnsupportedClauseOperation(BaseClauseExc):
    __template__: t.ClassVar[str] = "Clause {clause} is not supported"


class UnprocessableClause(BaseClauseExc):
    __template__: t.ClassVar[str] = "Clause {clause} can not be processed"
