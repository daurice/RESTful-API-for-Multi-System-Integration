import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_create_order(client):
    order_data = {
        "customer_id": "cust_001",
        "books": [{"book_id": "123", "quantity": 2}],
        "payment_method": "credit_card"
    }
    response = client.post("/api/orders", json=order_data, headers={"Authorization": "Bearer my_secure_token"})
    assert response.status_code == 201
    assert "order_id" in response.json

def test_get_order(client):
    # First create an order
    order_data = {
        "customer_id": "cust_002",
        "books": [{"book_id": "456", "quantity": 1}],
        "payment_method": "paypal"
    }
    create_response = client.post("/api/orders", json=order_data, headers={"Authorization": "Bearer my_secure_token"})
    order_id = create_response.json["order_id"]
    
    # Then retrieve it
    response = client.get(f"/api/orders/{order_id}", headers={"Authorization": "Bearer my_secure_token"})
    assert response.status_code == 200
    assert response.json["customer_id"] == "cust_002"

def test_create_order_insufficient_stock(client):
    order_data = {
        "customer_id": "cust_003",
        "books": [{"book_id": "123", "quantity": 1000}],
        "payment_method": "credit_card"
    }
    response = client.post("/api/orders", json=order_data, headers={"Authorization": "Bearer my_secure_token"})
    assert response.status_code == 400
