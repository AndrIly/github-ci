import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture()
def client():
    with TestClient(app) as c:
        yield c


def test_create_recipe(client):
    response = client.post(
        "/recipes",
        json={
            "title": "string",
            "description": "string",
            "time_cooking": 1,
            "ingredient": "string",
        },
    )
    assert response.status_code == 200

    data = response.json()

    assert data["id"] is not None
    assert data["title"] == "string"
    assert data["description"] == "string"
    assert data["time_cooking"] == 1
    assert data["ingredient"] == "string"
    assert data["count_watch"] == 0


def test_get_recipes(client):
    client.post(
        "/recipes",
        json={
            "title": "12",
            "description": "13",
            "time_cooking": 30,
            "ingredient": "14",
        },
    )

    response = client.get("/recipes")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    recipe = data[0]
    assert "id" in recipe
    assert "title" in recipe
    assert "count_watch" in recipe
    assert "time_cooking" in recipe


def test_get_recipe_detail(client):
    create_response = client.post(
        "/recipes",
        json={
            "title": "12",
            "description": "17",
            "time_cooking": 60,
            "ingredient": "2ffs",
        },
    )

    recipe_id = create_response.json()["id"]
    response = client.get(f"/recipes/{recipe_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == recipe_id
    assert data["title"] == "12"
    assert data["description"] == "17"
    assert data["ingredient"] == "2ffs"
    assert data["time_cooking"] == 60


def test_get_recipe_detail_increases_count_watch(client):
    create_response = client.post(
        "/recipes",
        json={
            "title": "klo",
            "description": "kll",
            "time_cooking": 10,
            "ingredient": "kllo",
        },
    )

    recipe_id = create_response.json()["id"]
    client.get(f"/recipes/{recipe_id}")
    client.get(f"/recipes/{recipe_id}")
    response = client.get("/recipes")
    recipes = response.json()
    target_recipe = None
    for recipe in recipes:
        if recipe["id"] == recipe_id:
            target_recipe = recipe
            break

    assert target_recipe is not None
    assert target_recipe["count_watch"] == 2


def test_get_recipe_not_found(client):
    response = client.get("/recipes/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Recipe not found"


def test_create_recipe_validation_error(client):
    response = client.post(
        "/recipes",
        json={
            "title": "",
            "description": "0",
            "time_cooking": 0,
            "ingredient": "0",
        },
    )

    assert response.status_code == 422
