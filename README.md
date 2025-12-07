# RESTful API for Multi-System Integration

A comprehensive Bookstore Management System demonstrating RESTful API design and multi-system integration.

## Project Overview

This project implements a RESTful API that integrates three subsystems:
- **Inventory System**: Manages book catalog and stock levels
- **Sales System**: Processes customer orders and payments
- **Delivery System**: Handles order fulfillment and tracking

## Features

- RESTful API design with proper HTTP methods and status codes
- JSON-based data exchange
- Token-based authentication
- Interactive Swagger/OpenAPI documentation
- Comprehensive unit tests
- Mock services for system simulation
- Complete integration flow

## Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

1. **Clone the repository**
```bash
cd RESTful-API-for-Multi-System-Integration
```

2. **Create virtual environment**
```bash
python -m venv flask_env
flask_env\Scripts\activate  # Windows
```

3. **Install dependencies**
```bash
cd bookstore_api
pip install -r requirements.txt
```

4. **Run the API**
```bash
python app.py
# Or use the batch script: run.bat
```

The API will be available at `http://localhost:5000`

### Access Documentation
Open your browser and navigate to:
```
http://localhost:5000/api/docs
```

## Documentation

- **[API Documentation](API_DOCUMENTATION.md)** - Complete API reference with examples
- **[Implementation Report](IMPLEMENTATION_REPORT.md)** - Design decisions and architecture
- **[Testing Guide](TESTING_GUIDE.md)** - Comprehensive testing instructions
- **[Bookstore API README](bookstore_api/README.md)** - Detailed usage guide

## Testing

### Run Unit Tests
```bash
cd bookstore_api
pytest
```

### Test with cURL
```bash
# List all books
curl -X GET "http://localhost:5000/api/books" \
  -H "Authorization: Bearer my_secure_token"

# Create an order
curl -X POST "http://localhost:5000/api/orders" \
  -H "Authorization: Bearer my_secure_token" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "cust_001",
    "books": [{"book_id": "123", "quantity": 2}],
    "payment_method": "credit_card"
  }'
```

### Test with Postman
Import `POSTMAN_COLLECTION.json` into Postman for ready-to-use API requests.

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

## Authentication

All endpoints require Bearer token authentication:
```
Authorization: Bearer my_secure_token
```

## Project Structure

```
RESTful-API-for-Multi-System-Integration/
├── bookstore_api/              # Main API application
│   ├── app.py                 # Flask application
│   ├── config.py              # Configuration
│   ├── requirements.txt       # Dependencies
│   ├── run.bat               # Windows start script
│   ├── data/                 # JSON data storage
│   │   ├── books.json
│   │   ├── orders.json
│   │   └── deliveries.json
│   ├── service/              # Business logic
│   │   ├── inventory.py
│   │   ├── sales.py
│   │   └── delivery.py
│   └── tests/                # Unit tests
│       ├── test_inventory.py
│       ├── test_sales.py
│       └── test_delivery.py
├── API_DOCUMENTATION.md       # API specifications
├── IMPLEMENTATION_REPORT.md   # Design report
├── TESTING_GUIDE.md          # Testing instructions
├── POSTMAN_COLLECTION.json   # Postman collection
└── README.md                 # This file
```

## Technology Stack

- **Framework**: Flask (Python)
- **Documentation**: Flasgger (Swagger/OpenAPI)
- **Testing**: Pytest
- **Data Format**: JSON
- **Authentication**: Bearer Token

## Sample Data

The system comes with pre-populated sample data:

**Books:**
- The Great Gatsby by F. Scott Fitzgerald ($15.99, 50 in stock)
- 1984 by George Orwell ($12.99, 30 in stock)
- To Kill a Mockingbird by Harper Lee ($14.99, 25 in stock)

## Integration Flow

1. **Check Inventory** → Verify book availability
2. **Create Order** → Process payment and reserve stock
3. **Create Delivery** → Schedule delivery
4. **Track Status** → Monitor order and delivery

## Learning Outcomes

This project demonstrates:
- RESTful API design principles
- Multi-system integration patterns
- Authentication and security
- API documentation best practices
- Test-driven development
- Clean code architecture

## Future Enhancements

- Database integration (PostgreSQL)
- JWT authentication
- Payment gateway integration
- Real-time notifications
- Microservices architecture
- Docker containerization
- CI/CD pipeline

## Deliverables

- Source code for API and mock services  
- API documentation (Swagger + Markdown)  
- Sample test cases and results  
- Implementation report (2-3 pages)  
- Postman collection for testing  
- Comprehensive README and guides  

## Contributing

This is an educational project demonstrating RESTful API design and multi-system integration.

## License

This project is for educational purposes.

## Author

Developed as a demonstration of RESTful API design and multi-system integration patterns.

---

**Need Help?** Check the documentation files or open the Swagger UI at `/api/docs`
