# Bookstore Management System - API Documentation

## Overview

This RESTful API provides endpoints for managing a bookstore's operations across three integrated subsystems: Inventory, Sales, and Delivery.

**Base URL**: `http://localhost:5000/api`

**Authentication**: Bearer Token (Header: `Authorization: Bearer my_secure_token`)

## Table of Contents

1. [Inventory System](#inventory-system)
2. [Sales System](#sales-system)
3. [Delivery System](#delivery-system)
4. [Error Responses](#error-responses)
5. [Data Models](#data-models)

---

## Inventory System

### List All Books

Retrieve all books in the inventory.

**Endpoint**: `GET /api/books`

**Headers**:
```
Authorization: Bearer my_secure_token
```

**Response** (200 OK):
```json
{
  "123": {
    "id": "123",
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "price": 15.99,
    "stock": 50,
    "isbn": "9780743273565"
  },
  "456": {
    "id": "456",
    "title": "1984",
    "author": "George Orwell",
    "price": 12.99,
    "stock": 30,
    "isbn": "9780451524935"
  }
}
```

### Get Book Details

Retrieve details of a specific book.

**Endpoint**: `GET /api/books/{book_id}`

**Path Parameters**:
- `book_id` (string, required): Unique book identifier

**Headers**:
```
Authorization: Bearer my_secure_token
```

**Response** (200 OK):
```json
{
  "id": "123",
  "title": "The Great Gatsby",
  "author": "F. Scott Fitzgerald",
  "price": 15.99,
  "stock": 50,
  "isbn": "9780743273565"
}
```

**Error Response** (404 Not Found):
```json
{
  "error": "Book not found"
}
```

---

## Sales System

### Create Order

Create a new customer order and process payment.

**Endpoint**: `POST /api/orders`

**Headers**:
```
Authorization: Bearer my_secure_token
Content-Type: application/json
```

**Request Body**:
```json
{
  "customer_id": "cust_001",
  "books": [
    {
      "book_id": "123",
      "quantity": 2
    },
    {
      "book_id": "456",
      "quantity": 1
    }
  ],
  "payment_method": "credit_card"
}
```

**Response** (201 Created):
```json
{
  "order_id": "order_1",
  "customer_id": "cust_001",
  "books": [
    {
      "book_id": "123",
      "quantity": 2
    },
    {
      "book_id": "456",
      "quantity": 1
    }
  ],
  "total_amount": 44.97,
  "status": "Confirmed",
  "payment_status": "Paid"
}
```

**Error Response** (400 Bad Request):
```json
{
  "error": "Book 123 not available or insufficient stock"
}
```

### Get Order Details

Retrieve details of a specific order.

**Endpoint**: `GET /api/orders/{order_id}`

**Path Parameters**:
- `order_id` (string, required): Unique order identifier

**Headers**:
```
Authorization: Bearer my_secure_token
```

**Response** (200 OK):
```json
{
  "order_id": "order_1",
  "customer_id": "cust_001",
  "books": [
    {
      "book_id": "123",
      "quantity": 2
    }
  ],
  "total_amount": 31.98,
  "status": "Confirmed",
  "payment_status": "Paid"
}
```

**Error Response** (404 Not Found):
```json
{
  "error": "Order not found"
}
```

---

## Delivery System

### Create Delivery

Create a delivery record for an order.

**Endpoint**: `POST /api/deliveries`

**Headers**:
```
Authorization: Bearer my_secure_token
Content-Type: application/json
```

**Request Body**:
```json
{
  "order_id": "order_1",
  "address": "123 Main St, City, State 12345",
  "estimated_delivery_date": "2024-12-31"
}
```

**Response** (201 Created):
```json
{
  "delivery_id": "del_1",
  "order_id": "order_1",
  "address": "123 Main St, City, State 12345",
  "status": "Pending",
  "estimated_delivery_date": "2024-12-31"
}
```

### Get Delivery Status

Retrieve delivery status and details.

**Endpoint**: `GET /api/deliveries/{delivery_id}`

**Path Parameters**:
- `delivery_id` (string, required): Unique delivery identifier

**Headers**:
```
Authorization: Bearer my_secure_token
```

**Response** (200 OK):
```json
{
  "delivery_id": "del_1",
  "order_id": "order_1",
  "address": "123 Main St, City, State 12345",
  "status": "Pending",
  "estimated_delivery_date": "2024-12-31"
}
```

**Error Response** (404 Not Found):
```json
{
  "error": "Delivery not found"
}
```

---

## Error Responses

### 401 Unauthorized

Missing or invalid authentication token.

```json
{
  "error": "Unauthorized"
}
```

### 400 Bad Request

Invalid request data or business logic error.

```json
{
  "error": "Descriptive error message"
}
```

### 404 Not Found

Requested resource does not exist.

```json
{
  "error": "Resource not found"
}
```

---

## Data Models

### Book

```json
{
  "id": "string",
  "title": "string",
  "author": "string",
  "price": "number",
  "stock": "integer",
  "isbn": "string"
}
```

### Order

```json
{
  "order_id": "string",
  "customer_id": "string",
  "books": [
    {
      "book_id": "string",
      "quantity": "integer"
    }
  ],
  "total_amount": "number",
  "status": "string",
  "payment_status": "string"
}
```

### Delivery

```json
{
  "delivery_id": "string",
  "order_id": "string",
  "address": "string",
  "status": "string",
  "estimated_delivery_date": "string (YYYY-MM-DD)"
}
```

---

## Integration Flow

### Complete Order Flow

1. **Check Inventory**: `GET /api/books/{book_id}` - Verify book availability
2. **Create Order**: `POST /api/orders` - Place order and process payment
3. **Create Delivery**: `POST /api/deliveries` - Schedule delivery
4. **Track Delivery**: `GET /api/deliveries/{delivery_id}` - Monitor delivery status

### Example Workflow

```bash
# Step 1: Check book availability
curl -X GET "http://localhost:5000/api/books/123" \
  -H "Authorization: Bearer my_secure_token"

# Step 2: Create order
curl -X POST "http://localhost:5000/api/orders" \
  -H "Authorization: Bearer my_secure_token" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "cust_001",
    "books": [{"book_id": "123", "quantity": 2}],
    "payment_method": "credit_card"
  }'

# Step 3: Create delivery (using order_id from step 2)
curl -X POST "http://localhost:5000/api/deliveries" \
  -H "Authorization: Bearer my_secure_token" \
  -H "Content-Type: application/json" \
  -d '{
    "order_id": "order_1",
    "address": "123 Main St, City, State 12345",
    "estimated_delivery_date": "2024-12-31"
  }'

# Step 4: Track delivery
curl -X GET "http://localhost:5000/api/deliveries/del_1" \
  -H "Authorization: Bearer my_secure_token"
```

---

## Testing with Postman

1. Import the API endpoints into Postman
2. Set up environment variable: `token = my_secure_token`
3. Add Authorization header: `Bearer {{token}}`
4. Test each endpoint with sample data

## Rate Limiting

Currently not implemented. Recommended for production:
- 100 requests per minute per IP
- 1000 requests per hour per API key

## Versioning

Current version: v1 (implicit in `/api` prefix)

Future versions will use: `/api/v2`, `/api/v3`, etc.
