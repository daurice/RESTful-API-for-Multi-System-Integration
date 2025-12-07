from flask import Flask, request, jsonify
from flasgger import Swagger
from config import API_TOKEN
from service import inventory, sales, delivery

app = Flask(__name__)
swagger_config = {
    "headers": [],
    "specs": [{
        "endpoint": 'apispec',
        "route": '/apispec.json',
        "rule_filter": lambda rule: True,
        "model_filter": lambda tag: True,
    }],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/api/docs"
}
Swagger(app, config=swagger_config)

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

# Inventory endpoints
@app.route("/api/books", methods=["GET"])
@require_auth
def list_books():
    """
    List All Books
    ---
    tags:
      - Inventory
    security:
      - Bearer: []
    responses:
      200:
        description: List of all books
    """
    books = inventory.get_all_books()
    return jsonify(books)

@app.route("/api/books/<book_id>", methods=["GET"])
@require_auth
def get_book(book_id):
    """
    Get Book Details
    ---
    tags:
      - Inventory
    security:
      - Bearer: []
    parameters:
      - name: book_id
        in: path
        type: string
        required: true
        description: Book ID
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

# Sales endpoints
@app.route("/api/orders", methods=["POST"])
@require_auth
def create_order():
    """
    Create Order
    ---
    tags:
      - Sales
    security:
      - Bearer: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - customer_id
            - books
            - payment_method
          properties:
            customer_id:
              type: string
              example: "cust_001"
            books:
              type: array
              items:
                type: object
                properties:
                  book_id:
                    type: string
                    example: "123"
                  quantity:
                    type: integer
                    example: 2
            payment_method:
              type: string
              example: "credit_card"
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

@app.route("/api/orders/<order_id>", methods=["GET"])
@require_auth
def get_order(order_id):
    """
    Get Order Details
    ---
    tags:
      - Sales
    security:
      - Bearer: []
    parameters:
      - name: order_id
        in: path
        type: string
        required: true
    responses:
      200:
        description: Order details
      404:
        description: Order not found
    """
    order = sales.get_order(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404
    return jsonify(order)

# Delivery endpoints
@app.route("/api/deliveries", methods=["POST"])
@require_auth
def create_delivery():
    """
    Create Delivery
    ---
    tags:
      - Delivery
    security:
      - Bearer: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - order_id
            - address
            - estimated_delivery_date
          properties:
            order_id:
              type: string
              example: "order_1"
            address:
              type: string
              example: "123 Main St, City, State 12345"
            estimated_delivery_date:
              type: string
              example: "2024-12-31"
    responses:
      201:
        description: Delivery created successfully
    """
    delivery_data = request.json
    deliv = delivery.create_delivery(delivery_data)
    return jsonify(deliv), 201

@app.route("/api/deliveries/<delivery_id>", methods=["GET"])
@require_auth
def get_delivery(delivery_id):
    """
    Get Delivery Status
    ---
    tags:
      - Delivery
    security:
      - Bearer: []
    parameters:
      - name: delivery_id
        in: path
        type: string
        required: true
    responses:
      200:
        description: Delivery details
      404:
        description: Delivery not found
    """
    deliv = delivery.get_delivery(delivery_id)
    if not deliv:
        return jsonify({"error": "Delivery not found"}), 404
    return jsonify(deliv)

if __name__ == "__main__":
    app.run(debug=True)
