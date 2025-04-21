import contextlib

import falcon
import sqlalchemy as sa

from kit_up.core import models
from kit_up.core.contexts import uow
from kit_up.core.domains import crud
from kit_up.core.stashes import base, context_vars
from kit_up.impl.falcon import crud as flcn
from kit_up.impl.falcon import errors
from kit_up.impl.sql_alchemy import contexts
from kit_up.impl.sql_alchemy import orm
from kit_up.impl.sql_alchemy import repositories


class MyStash(base.AbstractAttrStash, context_vars.ContextVarStash):
    pass


class AppContext(contexts.SqlalchemyContextMixin, uow.UowContextMixin):
    pass


class AppRepo(repositories.SqlalchemyCrudRepository):
    pass


class AppModel(models.BaseModel):
    id: int
    name: str
    surname: str


class BaseOrm(sa.orm.DeclarativeBase, orm.SqlalchemyAdapterMixin):
    pass


class AppOrm(BaseOrm):
    __tablename__ = "app_orm"

    id: sa.orm.Mapped[int] = sa.orm.MappedColumn(primary_key=True)
    name: sa.orm.Mapped[str] = sa.orm.MappedColumn()
    surname: sa.orm.Mapped[str] = sa.orm.MappedColumn()


class MyFalconApp(falcon.App, flcn.AddCrudRouteMixin):
    pass


class RootController:
    def on_get(self, req, resp):
        resp.media = ["cabinets"]


def main():
    stash = MyStash()
    ctx = AppContext(stash=stash)
    repo = AppRepo(context=ctx, model_type=AppModel, orm_type=AppOrm)
    domain = crud.CrudDomain(repository=repo)

    print("START: opening")
    ctx.uow_open()
    BaseOrm.metadata.create_all(ctx.sa_engine)
    print(f"OPENED: {ctx.uow}")
    views = domain.create(dict(name="John", surname="Johnson"))
    view = views[0]
    print(view)
    print(view.as_dict())
    print(domain.filter())
    ctx.uow.commit()
    print("pick")
    print(domain.pick(1))
    print("get_by")
    print(domain.get_by(name="John"))
    print("filter_by")
    print(domain.filter_by(name="John", surname="Snow"))
    ctx.uow_close()
    print("CLOSED")
    app = MyFalconApp(media_type=falcon.MEDIA_JSON)
    app.add_error_handler(errors.ApiError)
    app.add_route("/", RootController())
    # app.add_error_handler(Exception, )

    app.add_crud_route("/cabinets/", flcn.CrudController(domain=domain))

    from wsgiref.simple_server import make_server
    ctx.uow_open()
    with make_server('', 8001, app) as httpd:
        httpd.serve_forever()
    ctx.uow_close()

    use_case = ...
    access = ...


if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt):
        main()
