import pytest
from fastapi.testclient import TestClient

from app.main import app, db

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


@pytest.fixture
def seed_db():
    """Seed the database with some data for testing."""
    db_data = {
        1: {"name": "Foo", "description": "A foo item"},
        2: {"name": "Bar", "description": "A bar item"},
    }
    db.update(db_data)
    yield
    db.clear()


def test_read_item_success(seed_db):
    """Test reading an item that exists in the database."""
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json() == {"name": "Foo", "description": "A foo item"}


def test_read_item_not_found(seed_db):
    """Test reading an item that does not exist in the database."""
    response = client.get("/items/99")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}
