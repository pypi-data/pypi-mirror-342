from sqlalchemy.orm import session

from kit_up.core.mixins import require


class RequiresSqlalchemySessionMixin(
    require.RequiresMixin,
    requires="sa_session",
):
    _sa_session: session.Session
