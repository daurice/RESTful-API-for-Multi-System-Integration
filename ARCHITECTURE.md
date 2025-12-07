# System Architecture - Bookstore Management API

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Client Layer                         │
│  (Web Browser, Mobile App, Postman, cURL, Other Services)   │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/HTTPS
                         │ JSON
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                      API Gateway Layer                       │
│                    (Flask Application)                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           Authentication Middleware                   │  │
│  │              (Bearer Token)                          │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Routing & Endpoints                     │  │
│  │  /api/books, /api/orders, /api/deliveries          │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Service Layer                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Inventory   │  │    Sales     │  │   Delivery   │     │
│  │   Service    │◄─┤   Service    │  │   Service    │     │
│  │              │  │              │  │              │     │
│  │ - get_books  │  │ - create_ord │  │ - create_del │     │
│  │ - get_book   │  │ - get_order  │  │ - get_deliv  │     │
│  │ - update_stk │  │ - validate   │  │ - update_sts │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
│         │                  │                  │              │
└─────────┼──────────────────┼──────────────────┼──────────────┘
          │                  │                  │
          ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────┐
│                      Data Layer                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  books.json  │  │ orders.json  │  │deliveries.json│    │
│  │              │  │              │  │              │     │
│  │ Book catalog │  │ Order records│  │Delivery data │     │
│  │ & inventory  │  │ & payments   │  │& tracking    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

## Component Interaction Flow

### 1. Order Creation Flow

```
Client                API Layer           Sales Service      Inventory Service
  │                      │                      │                   │
  │  POST /api/orders    │                      │                   │
  ├─────────────────────►│                      │                   │
  │                      │  Authenticate        │                   │
  │                      ├──────────────┐       │                   │
  │                      │              │       │                   │
  │                      │◄─────────────┘       │                   │
  │                      │  create_order()      │                   │
  │                      ├─────────────────────►│                   │
  │                      │                      │  get_book()       │
  │                      │                      ├──────────────────►│
  │                      │                      │  Book details     │
  │                      │                      │◄──────────────────┤
  │                      │                      │  Validate stock   │
  │                      │                      ├──────────┐        │
  │                      │                      │          │        │
  │                      │                      │◄─────────┘        │
  │                      │                      │  update_stock()   │
  │                      │                      ├──────────────────►│
  │                      │                      │  Stock updated    │
  │                      │                      │◄──────────────────┤
  │                      │  Order created       │                   │
  │                      │◄─────────────────────┤                   │
  │  201 Created         │                      │                   │
  │◄─────────────────────┤                      │                   │
  │  {order_details}     │                      │                   │
```

### 2. Complete Purchase Flow

```
┌──────────┐
│  Client  │
└────┬─────┘
     │
     │ 1. GET /api/books/123
     │    Check availability
     ▼
┌──────────────┐
│  Inventory   │──► Returns: Book details, price, stock
│   System     │
└──────────────┘
     │
     │ 2. POST /api/orders
     │    Create order with payment
     ▼
┌──────────────┐
│    Sales     │──► Validates stock
│   System     │──► Calculates total
└──────┬───────┘    Processes payment
       │            Updates inventory
       │            Returns order_id
       │
       │ 3. POST /api/deliveries
       │    Schedule delivery
       ▼
┌──────────────┐
│   Delivery   │──► Creates delivery record
│   System     │──► Links to order_id
└──────┬───────┘    Sets estimated date
       │            Returns delivery_id
       │
       │ 4. GET /api/deliveries/{id}
       │    Track delivery
       ▼
┌──────────────┐
│   Client     │◄── Delivery status
└──────────────┘
```

## Data Models & Relationships

```
┌─────────────────────┐
│       Book          │
├─────────────────────┤
│ id: string          │
│ title: string       │
│ author: string      │
│ price: number       │
│ stock: integer      │◄────────┐
│ isbn: string        │         │
└─────────────────────┘         │
                                 │ References
                                 │
┌─────────────────────┐         │
│       Order         │         │
├─────────────────────┤         │
│ order_id: string    │◄────────┼────────┐
│ customer_id: string │         │        │
│ books: array        ├─────────┘        │
│   - book_id         │                  │
│   - quantity        │                  │
│ total_amount: num   │                  │
│ status: string      │                  │
│ payment_status: str │                  │
└─────────────────────┘                  │
                                          │ References
                                          │
┌─────────────────────┐                  │
│      Delivery       │                  │
├─────────────────────┤                  │
│ delivery_id: string │                  │
│ order_id: string    ├──────────────────┘
│ address: string     │
│ status: string      │
│ estimated_date: str │
└─────────────────────┘
```

## Authentication Flow

```
┌────────────┐
│   Client   │
└─────┬──────┘
      │
      │ Request with Authorization header
      │ Authorization: Bearer my_secure_token
      ▼
┌──────────────────────┐
│  Authentication      │
│  Middleware          │
└──────┬───────────────┘
       │
       │ Validate token
       ├──────────┐
       │          │
       ▼          ▼
   Valid?      Invalid?
     │            │
     │            └──► 401 Unauthorized
     │                 {"error": "Unauthorized"}
     │
     └──► Continue to endpoint
          Process request
          Return response
```

## API Endpoint Structure

```
/api
├── /books
│   ├── GET /              → List all books
│   └── GET /{book_id}     → Get book details
│
├── /orders
│   ├── POST /             → Create order
│   └── GET /{order_id}    → Get order details
│
└── /deliveries
    ├── POST /             → Create delivery
    └── GET /{delivery_id} → Get delivery status
```

## Technology Stack Layers

```
┌─────────────────────────────────────────┐
│         Presentation Layer              │
│  Swagger UI, Postman, cURL, Browsers    │
└─────────────────────────────────────────┘
                  ▲
                  │ HTTP/JSON
                  ▼
┌─────────────────────────────────────────┐
│         Application Layer               │
│  Flask Framework + Flasgger             │
│  - Routing                              │
│  - Request/Response handling            │
│  - Authentication                       │
└─────────────────────────────────────────┘
                  ▲
                  │
                  ▼
┌─────────────────────────────────────────┐
│         Business Logic Layer            │
│  Service Modules (Python)               │
│  - inventory.py                         │
│  - sales.py                             │
│  - delivery.py                          │
└─────────────────────────────────────────┘
                  ▲
                  │
                  ▼
┌─────────────────────────────────────────┐
│         Data Access Layer               │
│  JSON File Operations                   │
│  - Read/Write operations                │
│  - Data validation                      │
└─────────────────────────────────────────┘
                  ▲
                  │
                  ▼
┌─────────────────────────────────────────┐
│         Data Storage Layer              │
│  JSON Files (Mock Database)             │
│  - books.json                           │
│  - orders.json                          │
│  - deliveries.json                      │
└─────────────────────────────────────────┘
```

## Deployment Architecture (Production)

```
┌─────────────────────────────────────────────────────────┐
│                    Load Balancer                         │
│                   (AWS ELB / Nginx)                      │
└────────────┬────────────────────────┬────────────────────┘
             │                        │
             ▼                        ▼
┌─────────────────────┐    ┌─────────────────────┐
│   API Instance 1    │    │   API Instance 2    │
│   (Flask + Gunicorn)│    │   (Flask + Gunicorn)│
└──────────┬──────────┘    └──────────┬──────────┘
           │                          │
           └──────────┬───────────────┘
                      │
                      ▼
           ┌─────────────────────┐
           │   Database Server   │
           │   (PostgreSQL)      │
           └─────────────────────┘
                      │
                      ▼
           ┌─────────────────────┐
           │   Cache Layer       │
           │   (Redis)           │
           └─────────────────────┘
```

## Security Architecture

```
┌──────────────────────────────────────────┐
│            Security Layers               │
├──────────────────────────────────────────┤
│  1. HTTPS/TLS Encryption                 │
│     └─► Secure data in transit           │
├──────────────────────────────────────────┤
│  2. Authentication                       │
│     └─► Bearer Token validation          │
├──────────────────────────────────────────┤
│  3. Authorization                        │
│     └─► Role-based access control        │
├──────────────────────────────────────────┤
│  4. Input Validation                     │
│     └─► Sanitize user inputs             │
├──────────────────────────────────────────┤
│  5. Rate Limiting                        │
│     └─► Prevent abuse                    │
├──────────────────────────────────────────┤
│  6. Logging & Monitoring                 │
│     └─► Track suspicious activity        │
└──────────────────────────────────────────┘
```

## Scalability Considerations

### Horizontal Scaling
```
Single Instance          Multiple Instances
┌──────────┐            ┌──────────┐ ┌──────────┐ ┌──────────┐
│   API    │     →      │  API 1   │ │  API 2   │ │  API 3   │
└──────────┘            └──────────┘ └──────────┘ └──────────┘
                               │           │           │
                               └───────────┴───────────┘
                                          │
                                   ┌──────────────┐
                                   │   Database   │
                                   └──────────────┘
```

### Microservices Evolution
```
Monolithic API              Microservices
┌────────────────┐         ┌──────────────┐
│                │         │  Inventory   │
│  Bookstore API │   →     │  Service     │
│                │         └──────────────┘
│  - Inventory   │         ┌──────────────┐
│  - Sales       │         │    Sales     │
│  - Delivery    │         │   Service    │
│                │         └──────────────┘
└────────────────┘         ┌──────────────┐
                           │   Delivery   │
                           │   Service    │
                           └──────────────┘
```

## Error Handling Flow

```
Request → Validation → Business Logic → Response
   │          │              │             │
   │          ▼              │             │
   │      Invalid?           │             │
   │          │              │             │
   │          └──► 400 Bad Request         │
   │                         │             │
   │                         ▼             │
   │                    Error occurs?      │
   │                         │             │
   │                         └──► 500 Internal Error
   │                                       │
   └───────────────────────────────────────┘
                Success → 200/201
```

## Monitoring & Observability

```
┌─────────────────────────────────────────┐
│              Application                 │
│         (Bookstore API)                  │
└────────┬────────────────────┬────────────┘
         │                    │
         │ Logs               │ Metrics
         ▼                    ▼
┌─────────────────┐  ┌─────────────────┐
│  Log Aggregator │  │  Metrics Store  │
│  (ELK Stack)    │  │  (Prometheus)   │
└────────┬────────┘  └────────┬────────┘
         │                    │
         └──────────┬─────────┘
                    ▼
         ┌─────────────────────┐
         │   Dashboard         │
         │   (Grafana)         │
         └─────────────────────┘
```

---

This architecture provides a solid foundation for a scalable, maintainable, and secure bookstore management system.
