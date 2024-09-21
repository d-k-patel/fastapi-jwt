from fastapi.testclient import TestClient

from main import app
from schemas import Band

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"hello": "world"}


def test_get_bands():
    response = client.get("/bands")
    data = response.json()
    assert response.status_code == 200
    assert isinstance(data, list)


def test_create_band():
    band = Band(
        id=6,
        name="The Beatles",
        genre="Rock",
        members=["John Lennon", "Paul McCartney", "George Harrison", "Ringo Starr"],
    )
    response = client.post("/bands", json=band.model_dump())
    assert response.status_code == 201
    data = response.json()
    assert isinstance(data, dict)
    assert data["id"] == band.id
    assert data["name"] == band.name
    assert data["genre"] == band.genre
    assert data["members"] == band.members
