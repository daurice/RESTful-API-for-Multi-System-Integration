# Testing Guide - Bookstore Management System API

## Overview

This guide provides instructions for testing the Bookstore Management System API using various tools and methods.

---

## 1. Running Unit Tests

### Prerequisites
```bash
pip install pytest
```

### Execute All Tests
```bash
cd bookstore_api
pytest
```

### Run Specific Test Files
```bash
pytest tests/test_inventory.py
pytest tests/test_sales.py
pytest tests/test_delivery.py
```

### Verbose Output
```bash
pytest -v
```

### Test Coverage
```bash
pytest --cov=service --cov-report=html
```

---

## 2. Testing with cURL

### Setup
Ensure the API is running:
```bash
python app.py
```

### Test Cases

#### 2.1 List All Books
```bash
curl -X GET "http://localhost:5000/api/books" \
  -H "Authorization: Bearer my_secure_token"
```

**Expected Response** (200 OK):
```json
{
  "123": {
    "id": "123",
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "price": 15.99,
    "stock": 50,
    "isbn": "9780743273565"
  }
}
```

#### 2.2 Get Specific Book
```bash
curl -X GET "http://localhost:5000/api/books/123" \
  -H "Authorization: Bearer my_secure_token"
```

#### 2.3 Test Authentication Failure
```bash
curl -X GET "http://localhost:5000/api/books/123"
```

**Expected Response** (401 Unauthorized):
```json
{
  "error": "Unauthorized"
}
```

#### 2.4 Create Order
```bash
curl -X POST "http://localhost:5000/api/orders" \
  -H "Authorization: Bearer my_secure_token" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "cust_001",
    "books": [
      {"book_id": "123", "quantity": 2}
    ],
    "payment_method": "credit_card"
  }'
```

**Expected Response** (201 Created):
```json
{
  "order_id": "order_1",
  "customer_id": "cust_001",
  "books": [{"book_id": "123", "quantity": 2}],
  "total_amount": 31.98,
  "status": "Confirmed",
  "payment_status": "Paid"
}
```

#### 2.5 Get Order Details
```bash
curl -X GET "http://localhost:5000/api/orders/order_1" \
  -H "Authorization: Bearer my_secure_token"
```

#### 2.6 Create Delivery
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

#### 2.7 Get Delivery Status
```bash
curl -X GET "http://localhost:5000/api/deliveries/del_1" \
  -H "Authorization: Bearer my_secure_token"
```

---

## 3. Testing with Postman

### Setup Collection

1. **Create New Collection**: "Bookstore API"

2. **Set Environment Variables**:
   - `base_url`: `http://localhost:5000`
   - `token`: `my_secure_token`

3. **Configure Authorization**:
   - Type: Bearer Token
   - Token: `{{token}}`

### Test Requests

#### Request 1: List Books
- Method: GET
- URL: `{{base_url}}/api/books`
- Headers: Authorization: Bearer {{token}}

#### Request 2: Get Book
- Method: GET
- URL: `{{base_url}}/api/books/123`
- Headers: Authorization: Bearer {{token}}

#### Request 3: Create Order
- Method: POST
- URL: `{{base_url}}/api/orders`
- Headers: 
  - Authorization: Bearer {{token}}
  - Content-Type: application/json
- Body (raw JSON):
```json
{
  "customer_id": "cust_001",
  "books": [
    {"book_id": "123", "quantity": 2}
  ],
  "payment_method": "credit_card"
}
```

#### Request 4: Create Delivery
- Method: POST
- URL: `{{base_url}}/api/deliveries`
- Headers: 
  - Authorization: Bearer {{token}}
  - Content-Type: application/json
- Body (raw JSON):
```json
{
  "order_id": "order_1",
  "address": "123 Main St, City, State 12345",
  "estimated_delivery_date": "2024-12-31"
}
```

### Postman Tests Scripts

Add to each request's "Tests" tab:

```javascript
// Test status code
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

// Test response time
pm.test("Response time is less than 500ms", function () {
    pm.expect(pm.response.responseTime).to.be.below(500);
});

// Test JSON response
pm.test("Response is JSON", function () {
    pm.response.to.be.json;
});
```

---

## 4. Testing with Swagger UI

### Access Swagger Documentation
1. Start the API: `python app.py`
2. Open browser: `http://localhost:5000/api/docs`

### Interactive Testing

1. **Authorize**:
   - Click "Authorize" button
   - Enter: `my_secure_token`
   - Click "Authorize"

2. **Test Endpoints**:
   - Expand any endpoint
   - Click "Try it out"
   - Fill in parameters
   - Click "Execute"
   - View response

---

## 5. Integration Testing Scenarios

### Scenario 1: Complete Order Flow

```bash
# Step 1: Check book availability
curl -X GET "http://localhost:5000/api/books/123" \
  -H "Authorization: Bearer my_secure_token"

# Step 2: Create order
ORDER_RESPONSE=$(curl -X POST "http://localhost:5000/api/orders" \
  -H "Authorization: Bearer my_secure_token" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "cust_001",
    "books": [{"book_id": "123", "quantity": 2}],
    "payment_method": "credit_card"
  }')

# Extract order_id (using jq)
ORDER_ID=$(echo $ORDER_RESPONSE | jq -r '.order_id')

# Step 3: Create delivery
curl -X POST "http://localhost:5000/api/deliveries" \
  -H "Authorization: Bearer my_secure_token" \
  -H "Content-Type: application/json" \
  -d "{
    \"order_id\": \"$ORDER_ID\",
    \"address\": \"123 Main St, City, State 12345\",
    \"estimated_delivery_date\": \"2024-12-31\"
  }"

# Step 4: Verify order
curl -X GET "http://localhost:5000/api/orders/$ORDER_ID" \
  -H "Authorization: Bearer my_secure_token"
```

### Scenario 2: Insufficient Stock

```bash
curl -X POST "http://localhost:5000/api/orders" \
  -H "Authorization: Bearer my_secure_token" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "cust_002",
    "books": [{"book_id": "123", "quantity": 1000}],
    "payment_method": "credit_card"
  }'
```

**Expected**: 400 Bad Request with error message

### Scenario 3: Invalid Book ID

```bash
curl -X GET "http://localhost:5000/api/books/999" \
  -H "Authorization: Bearer my_secure_token"
```

**Expected**: 404 Not Found

---

## 6. Test Results Documentation

### Sample Test Results

```
======================== test session starts ========================
platform win32 -- Python 3.9.0
collected 10 items

tests/test_inventory.py ....                                  [ 40%]
tests/test_sales.py ...                                       [ 70%]
tests/test_delivery.py ..                                     [100%]

======================== 10 passed in 2.34s =========================
```

### Expected Test Coverage

| Module | Coverage |
|--------|----------|
| inventory.py | 95%+ |
| sales.py | 90%+ |
| delivery.py | 90%+ |
| app.py | 85%+ |

---

## 7. Performance Testing

### Load Testing with Apache Bench

```bash
# Install Apache Bench (comes with Apache)
# Test 1000 requests with 10 concurrent connections
ab -n 1000 -c 10 -H "Authorization: Bearer my_secure_token" \
  http://localhost:5000/api/books
```

### Expected Performance
- Response time: < 100ms for GET requests
- Response time: < 200ms for POST requests
- Throughput: > 100 requests/second

---

## 8. Troubleshooting

### Common Issues

**Issue**: 401 Unauthorized
- **Solution**: Check Authorization header format: `Bearer my_secure_token`

**Issue**: 404 Not Found
- **Solution**: Verify endpoint URL and resource ID

**Issue**: 400 Bad Request
- **Solution**: Validate JSON payload format and required fields

**Issue**: Connection Refused
- **Solution**: Ensure API is running: `python app.py`

### Debug Mode

Enable Flask debug mode for detailed error messages:
```python
app.run(debug=True)
```

---

## 9. Continuous Integration

### GitHub Actions Example

```yaml
name: API Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest -v
```

---

## 10. Test Checklist

- [ ] All unit tests pass
- [ ] Authentication works correctly
- [ ] All endpoints return correct status codes
- [ ] Error handling works as expected
- [ ] Data validation is enforced
- [ ] Integration flow works end-to-end
- [ ] Performance meets requirements
- [ ] Documentation is accurate
- [ ] Swagger UI is functional

---

## Conclusion

This testing guide covers comprehensive testing strategies for the Bookstore Management System API. Regular testing ensures API reliability, security, and performance.
