from flask import Flask, request, jsonify
from flasgger import Swagger
from config import API_TOKEN
from service import inventory, sales, delivery

app = Flask(__name__)
Swagger(app)

# Authentication decorator
def require_auth(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if token != f"Bearer " + API_TOKEN:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated

# Inventory endpoint
@app.route("/books/<book_id>", methods=["GET"])
@require_auth
def get_book(book_id):
    """
    Get Book Details
    ---
    parameters:
      - name: book_id
        in: path
        type: string
        required: true
    responses:
      200:
        description: Book details retrieved
      404:
        description: Book not found
    """
    book = inventory.get_book(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(book)

# Sales endpoint
@app.route("/orders", methods=["POST"])
@require_auth
def create_order():
    """
    Create Order
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            customer_id:
              type: string
            books:
              type: array
              items:
                type: object
                properties:
                  book_id: string
                  quantity: integer
            payment_method: string
    responses:
      201:
        description: Order created successfully
      400:
        description: Error in order creation
    """
    order_data = request.json
    order, error = sales.create_order(order_data)
    if error:
        return jsonify({"error": error}), 400
    return jsonify(order), 201

# Delivery endpoint
@app.route("/deliveries", methods=["POST"])
@require_auth
def create_delivery():
    """
    Create Delivery
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            order_id:
              type: string
            address:
              type: string
            estimated_delivery_date:
              type: string
    responses:
      201:
        description: Delivery created successfully
    """
    delivery_data = request.json
    deliv = delivery.create_delivery(delivery_data)
    return jsonify(deliv), 201

if __name__ == "__main__":
    app.run(debug=True)
