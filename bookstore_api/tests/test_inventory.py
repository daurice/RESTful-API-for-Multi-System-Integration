import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_book(client):
    response = client.get("/books/123", headers={"Authorization": "Bearer my_secure_token"})
    assert response.status_code == 200
    assert response.json["title"] == "The Great Gatsby"
