import http

import pytest

from kit_up.core.domains import exceptions as dom_excs
from kit_up.impl.falcon import errors


def test_retrieve(sync_client, sync_domain, fake_model_init):
    """Test base retrieve of model."""
    expected_entity_data = fake_model_init
    # Create another record for test filtering
    sync_domain.create(dict(id=2, name="Ark", surname="Survive"))

    resp = sync_client.get(f"/users/{fake_model_init['id']}")

    assert resp.status_code == http.HTTPStatus.OK
    assert resp.json == expected_entity_data


def test_retrieve_404(sync_client):
    """Test 404 error for retrieve of not exist model."""
    identity = 1
    expected_error = errors.NotFoundError(
        description=f"Entry with identity id={identity} not found",
    )

    resp = sync_client.get(f"/users/{identity}")

    assert resp.status_code == http.HTTPStatus.NOT_FOUND
    assert resp.json == {
        "title": expected_error.title,
        "description": expected_error.description,
    }


def test_listing(sync_client, sync_domain, fake_model_init):
    """Test base retrieve of model."""
    # Create another record for test filtering
    another_model_data = dict(id=2, name="Ark", surname="Survive")
    sync_domain.create(another_model_data)
    expected_resp = [fake_model_init, another_model_data]

    resp = sync_client.get("/users")

    assert resp.status_code == http.HTTPStatus.OK
    assert resp.json == expected_resp


def test_update(sync_client, fake_model_init):
    """Test update of model."""
    model_data = fake_model_init
    model_data["name"] = "New"
    model_data["surname"] = "Data"

    resp = sync_client.put(f"/users/{fake_model_init['id']}", json=model_data)

    assert resp.status_code == http.HTTPStatus.OK
    assert resp.json == model_data


def test_update_fields_validation(sync_client, fake_model_init):
    """
    Test update fields validation.

    Controller must validate that all fields are present.
    """
    expected_error_data = {
        "title": "BadRequestError",
        "description": "Missed fields: id,surname",
    }

    resp = sync_client.put(f"/users/{fake_model_init['id']}", json={"name": "New"})

    assert resp.status_code == http.HTTPStatus.BAD_REQUEST
    assert resp.json == expected_error_data


def test_update_404(sync_client):
    """Test 404 error for full update if entity not found."""
    identity = 1
    expected_error = errors.NotFoundError(
        description=f"Entry with identity id={identity} not found",
    )

    resp = sync_client.put(
        f"/users/{identity}",
        json={"id": identity, "name": "New", "surname": "Error"},
    )

    assert resp.status_code == http.HTTPStatus.NOT_FOUND
    assert resp.json == {
        "title": expected_error.title,
        "description": expected_error.description,
    }


def test_patch(sync_client, fake_model_init):
    """Test partial update of model."""
    model_data = fake_model_init
    patch_data = {"name": "New"}
    expected_resp_data = model_data | patch_data

    resp = sync_client.patch(f"/users/{fake_model_init['id']}", json=patch_data)

    assert resp.status_code == http.HTTPStatus.OK
    assert resp.json == expected_resp_data


def test_patch_404(sync_client):
    """Test 404 error for partial update if entity not found."""
    identity = 1
    expected_error = errors.NotFoundError(
        description=f"Entry with identity id={identity} not found",
    )

    resp = sync_client.patch(f"/users/{identity}", json={"name": "New"})

    assert resp.status_code == http.HTTPStatus.NOT_FOUND
    assert resp.json == {
        "title": expected_error.title,
        "description": expected_error.description,
    }


def test_delete(sync_client, sync_domain, fake_model_init):
    """Test delete of model."""
    identity = fake_model_init["id"]

    resp = sync_client.delete(f"/users/{identity}")

    assert resp.status_code == http.HTTPStatus.NO_CONTENT
    assert resp.json is None
    with pytest.raises(dom_excs.EntityNotFoundExc):
        sync_domain.pick(identity)
