from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_read_item():
    response = client.get("/items/42?q=testquery")
    assert response.status_code == 200
    assert response.json() == {
        "item_id": 42,
        "q": "testquery",
    }

def test_read_item_no_query():
    response = client.get("/items/42")
    assert response.status_code == 200
    assert response.json() == {
        "item_id": 42,
        "q": None,
    }
