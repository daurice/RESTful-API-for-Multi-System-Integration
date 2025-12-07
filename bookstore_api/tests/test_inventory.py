import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_list_books(client):
    response = client.get("/api/books", headers={"Authorization": "Bearer my_secure_token"})
    assert response.status_code == 200
    assert "123" in response.json

def test_get_book(client):
    response = client.get("/api/books/123", headers={"Authorization": "Bearer my_secure_token"})
    assert response.status_code == 200
    assert response.json["title"] == "The Great Gatsby"

def test_get_book_not_found(client):
    response = client.get("/api/books/999", headers={"Authorization": "Bearer my_secure_token"})
    assert response.status_code == 404

def test_unauthorized_access(client):
    response = client.get("/api/books/123")
    assert response.status_code == 401
