import json
from config import DATA_PATH
from service.inventory import update_stock, get_book

def load_orders():
    with open(DATA_PATH + "orders.json", "r") as f:
        return json.load(f)

def save_orders(orders):
    with open(DATA_PATH + "orders.json", "w") as f:
        json.dump(orders, f, indent=4)

def create_order(order_data):
    orders = load_orders()
    order_id = f"order_{len(orders) + 1}"
    total_amount = 0

    for item in order_data["books"]:
        book = get_book(item["book_id"])
        if not book or book["stock"] < item["quantity"]:
            return None, f"Book {item['book_id']} not available or insufficient stock"
        total_amount += book["price"] * item["quantity"]

    orders[order_id] = {
        "order_id": order_id,
        "customer_id": order_data["customer_id"],
        "books": order_data["books"],
        "total_amount": total_amount,
        "status": "Confirmed",
        "payment_status": "Paid"
    }

    # Update inventory
    for item in order_data["books"]:
        update_stock(item["book_id"], item["quantity"])

    save_orders(orders)
    return orders[order_id], None
