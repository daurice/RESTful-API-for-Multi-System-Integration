# Bookstore Management System - RESTful API

A comprehensive RESTful API for managing a bookstore's inventory, sales, and delivery systems.

## Features

- **Inventory Management**: Track books, stock levels, and details
- **Sales Processing**: Create and manage customer orders with payment processing
- **Delivery Tracking**: Manage order deliveries and track status
- **Authentication**: Token-based API authentication
- **API Documentation**: Interactive Swagger UI documentation

## Architecture

The system integrates three subsystems:
- **Inventory System**: Manages book catalog and stock
- **Sales System**: Processes orders and payments
- **Delivery System**: Handles order fulfillment and tracking

## Installation

1. Create and activate virtual environment:
```bash
python -m venv flask_env
flask_env\Scripts\activate  # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the API

```bash
cd bookstore_api
python app.py
```

The API will be available at `http://localhost:5000`

## API Documentation

Access interactive Swagger documentation at: `http://localhost:5000/api/docs`

## Authentication

All endpoints require Bearer token authentication. Include the token in the Authorization header:

```
Authorization: Bearer my_secure_token
```

## API Endpoints

### Inventory System

- `GET /api/books` - List all books
- `GET /api/books/{book_id}` - Get book details

### Sales System

- `POST /api/orders` - Create new order
- `GET /api/orders/{order_id}` - Get order details

### Delivery System

- `POST /api/deliveries` - Create delivery
- `GET /api/deliveries/{delivery_id}` - Get delivery status

## Usage Examples

### 1. List All Books
```bash
curl -X GET "http://localhost:5000/api/books" \
  -H "Authorization: Bearer my_secure_token"
```

### 2. Get Book Details
```bash
curl -X GET "http://localhost:5000/api/books/123" \
  -H "Authorization: Bearer my_secure_token"
```

### 3. Create Order
```bash
curl -X POST "http://localhost:5000/api/orders" \
  -H "Authorization: Bearer my_secure_token" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "cust_001",
    "books": [{"book_id": "123", "quantity": 2}],
    "payment_method": "credit_card"
  }'
```

### 4. Create Delivery
```bash
curl -X POST "http://localhost:5000/api/deliveries" \
  -H "Authorization: Bearer my_secure_token" \
  -H "Content-Type: application/json" \
  -d '{
    "order_id": "order_1",
    "address": "123 Main St, City, State 12345",
    "estimated_delivery_date": "2024-12-31"
  }'
```

## Testing

Run all tests:
```bash
pytest
```

Run specific test file:
```bash
pytest tests/test_inventory.py
```

## Data Storage

The API uses JSON files for data persistence:
- `data/books.json` - Book inventory
- `data/orders.json` - Customer orders
- `data/deliveries.json` - Delivery records

## Project Structure

```
bookstore_api/
├── app.py              # Main Flask application
├── config.py           # Configuration settings
├── requirements.txt    # Python dependencies
├── data/              # JSON data storage
│   ├── books.json
│   ├── orders.json
│   └── deliveries.json
├── service/           # Business logic
│   ├── inventory.py
│   ├── sales.py
│   └── delivery.py
└── tests/             # Unit tests
    ├── test_inventory.py
    ├── test_sales.py
    └── test_delivery.py
```

## Security Considerations

- Change the default API token in `config.py` for production
- Use HTTPS in production environments
- Implement rate limiting for production use
- Add input validation and sanitization
- Use environment variables for sensitive configuration

## Future Enhancements

- Database integration (PostgreSQL/MySQL)
- User authentication and authorization
- Order cancellation and refunds
- Inventory alerts for low stock
- Delivery tracking updates
- Email notifications
- Payment gateway integration
