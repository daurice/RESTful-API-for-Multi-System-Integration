import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_create_delivery(client):
    delivery_data = {
        "order_id": "order_1",
        "address": "123 Main St, City, State 12345",
        "estimated_delivery_date": "2024-12-31"
    }
    response = client.post("/api/deliveries", json=delivery_data, headers={"Authorization": "Bearer my_secure_token"})
    assert response.status_code == 201
    assert "delivery_id" in response.json

def test_get_delivery(client):
    # First create a delivery
    delivery_data = {
        "order_id": "order_2",
        "address": "456 Oak Ave, Town, State 67890",
        "estimated_delivery_date": "2024-12-25"
    }
    create_response = client.post("/api/deliveries", json=delivery_data, headers={"Authorization": "Bearer my_secure_token"})
    delivery_id = create_response.json["delivery_id"]
    
    # Then retrieve it
    response = client.get(f"/api/deliveries/{delivery_id}", headers={"Authorization": "Bearer my_secure_token"})
    assert response.status_code == 200
    assert response.json["order_id"] == "order_2"
