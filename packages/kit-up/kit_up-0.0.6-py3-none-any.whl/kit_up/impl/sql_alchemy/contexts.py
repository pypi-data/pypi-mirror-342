import functools

from sqlalchemy import engine

from kit_up.core.contexts import base


class SqlalchemyContextMixin(base.AbstractContext):
    session: str

    def __init__(self, *, sa_conf="sqlite://", **kwargs):
        # self.__engine = sa.engine.create_engine(sa_conf.engine.url)
        # self.__factory = sa.Session(self.__engine)
        self.__sa_conf = sa_conf
        super().__init__(**kwargs)

    @functools.cached_property
    def sa_engine(self):
        return engine.create_engine(self.__sa_conf, echo=True)


# >>> from sqlalchemy import create_engine
# >>> from sqlalchemy.orm import Session
# >>> engine = create_engine("sqlite://", echo=True)
# >>> with Session(engine) as session:
