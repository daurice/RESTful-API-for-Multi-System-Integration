# Quick Reference Card - Bookstore Management API

## 🚀 Quick Start

```bash
# Setup (first time only)
setup.bat

# Start API
cd bookstore_api
python app.py
```

**API URL**: `http://localhost:5000`  
**Docs**: `http://localhost:5000/api/docs`  
**Token**: `my_secure_token`

---

## 📡 API Endpoints

### Inventory System

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/books` | List all books |
| GET | `/api/books/{id}` | Get book details |

### Sales System

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/orders` | Create order |
| GET | `/api/orders/{id}` | Get order details |

### Delivery System

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/deliveries` | Create delivery |
| GET | `/api/deliveries/{id}` | Get delivery status |

---

## 🔐 Authentication

**Header**: `Authorization: Bearer my_secure_token`

---

## 📝 Sample Requests

### List Books
```bash
curl -X GET "http://localhost:5000/api/books" \
  -H "Authorization: Bearer my_secure_token"
```

### Get Book
```bash
curl -X GET "http://localhost:5000/api/books/123" \
  -H "Authorization: Bearer my_secure_token"
```

### Create Order
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

### Create Delivery
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

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_inventory.py

# Verbose output
pytest -v
```

---

## 📊 HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success (GET) |
| 201 | Created (POST) |
| 400 | Bad Request |
| 401 | Unauthorized |
| 404 | Not Found |

---

## 📚 Sample Data

### Books
- **123**: The Great Gatsby ($15.99, 50 in stock)
- **456**: 1984 ($12.99, 30 in stock)
- **789**: To Kill a Mockingbird ($14.99, 25 in stock)

---

## 🔄 Complete Workflow

```
1. GET /api/books/123          → Check availability
2. POST /api/orders            → Create order (returns order_id)
3. POST /api/deliveries        → Schedule delivery (use order_id)
4. GET /api/deliveries/{id}    → Track delivery
```

---

## 📖 Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | Project overview |
| `API_DOCUMENTATION.md` | Complete API reference |
| `IMPLEMENTATION_REPORT.md` | Design & implementation |
| `TESTING_GUIDE.md` | Testing instructions |
| `ARCHITECTURE.md` | System architecture |
| `PROJECT_SUMMARY.md` | Project summary |

---

## 🛠️ Project Structure

```
bookstore_api/
├── app.py              # Main API
├── config.py           # Configuration
├── service/            # Business logic
│   ├── inventory.py
│   ├── sales.py
│   └── delivery.py
├── data/               # Mock data
│   ├── books.json
│   ├── orders.json
│   └── deliveries.json
└── tests/              # Unit tests
    ├── test_inventory.py
    ├── test_sales.py
    └── test_delivery.py
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| 401 Unauthorized | Check Authorization header |
| 404 Not Found | Verify endpoint URL and ID |
| 400 Bad Request | Validate JSON payload |
| Connection refused | Ensure API is running |

---

## 💡 Tips

- Use Swagger UI for interactive testing: `/api/docs`
- Import `POSTMAN_COLLECTION.json` for Postman
- Check `TESTING_GUIDE.md` for detailed examples
- Enable debug mode: `app.run(debug=True)`

---

## 📞 Quick Links

- **Swagger UI**: http://localhost:5000/api/docs
- **GitHub Actions**: `.github/workflows/python-app.yml`
- **Postman Collection**: `POSTMAN_COLLECTION.json`

---

**Need Help?** Check the comprehensive documentation files or use Swagger UI for interactive exploration!
