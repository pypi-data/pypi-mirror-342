import typing as t

import falcon
import pytest
from falcon import asgi as falcon_asgi
from falcon import testing as ft

from kit_up.core import models
from kit_up.core.clauses import base as bfs
from kit_up.core.clauses import predicates as dfs
from kit_up.core.data_mappers import base as mappers
from kit_up.core.domains import crud as dom_crud
from kit_up.core.repositories import crud as repo_crud
from kit_up.impl.falcon import crud as flcn
from kit_up.impl.falcon import errors


class SyncFalconApp(falcon.App, flcn.AddCrudRouteMixin):
    pass


class _UserData(models.BaseModel):
    id: int
    name: str
    surname: str


class _AppModel(models.BaseModel):
    id: int
    name: str
    surname: str


def _clauses_to_ids_filter(*clauses) -> set[int]:
    ids_filters = set()
    for clause in clauses:
        if (
            isinstance(clause, dfs.Eq)
            and clause.value
            and clause.field == _AppModel.get_identity_qualifier()
        ):
            ids_filters.add(int(clause.value))
    return ids_filters


def _filter_by_clauses(store: dict[int, _UserData], *clauses) -> list[_UserData]:
    ids_filters = _clauses_to_ids_filter(*clauses)
    if ids_filters:
        return [entry for identity, entry in store.items() if identity in ids_filters]
    return list(store.values())


class Repository(repo_crud.AbstractBaseSemiCrudRepository):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._store: dict[int, _UserData] = {}

    def _create(self, inputs) -> t.Any:
        self._store.update({item.id: item for item in inputs})
        return inputs

    def _filter(self, *clauses: bfs.BaseClause):
        return _filter_by_clauses(self._store, *clauses)

    def update(self, model, *models) -> None:
        for m in (model, *models):
            self._store[m.id] = m

    def _erase(self, *filters: dfs.AbstractPredicateClause) -> t.Any:
        ids_filters = _clauses_to_ids_filter(self._store, *filters)
        if ids_filters:
            self._store = dict(
                filter(lambda item: item[0] not in ids_filters, self._store.items())
            )


@pytest.fixture
def sync_repo() -> Repository:
    return Repository(data_mapper=mappers.BaseDataMapper(_AppModel, _UserData))


@pytest.fixture
def sync_domain(sync_repo) -> dom_crud.CrudDomain:
    return dom_crud.CrudDomain(repository=sync_repo)


@pytest.fixture
def fake_model_init(sync_repo) -> dict[str, t.Any]:
    model_data = dict(id=1, name="test", surname="test2")
    sync_repo.create(model_data)
    return model_data


@pytest.fixture
def sync_app(sync_domain) -> falcon.App:
    app = SyncFalconApp(media_type=falcon.MEDIA_JSON)
    app.add_error_handler(errors.ApiError)
    app.add_crud_route("/users/", flcn.CrudController(domain=sync_domain))
    return app


@pytest.fixture
def async_app() -> falcon_asgi.App:
    raise NotImplementedError


@pytest.fixture
def sync_client(sync_app) -> ft.TestClient:
    return ft.TestClient(sync_app)
