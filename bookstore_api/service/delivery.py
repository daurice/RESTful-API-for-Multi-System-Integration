import json
from config import DATA_PATH

def load_deliveries():
    with open(DATA_PATH + "deliveries.json", "r") as f:
        return json.load(f)

def save_deliveries(deliveries):
    with open(DATA_PATH + "deliveries.json", "w") as f:
        json.dump(deliveries, f, indent=4)

def create_delivery(delivery_data):
    deliveries = load_deliveries()
    delivery_id = f"del_{len(deliveries) + 1}"

    deliveries[delivery_id] = {
        "delivery_id": delivery_id,
        "order_id": delivery_data["order_id"],
        "address": delivery_data["address"],
        "status": "Pending",
        "estimated_delivery_date": delivery_data["estimated_delivery_date"]
    }

    save_deliveries(deliveries)
    return deliveries[delivery_id]
