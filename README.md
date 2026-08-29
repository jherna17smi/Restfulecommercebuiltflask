# E-commerce API (Flask + MySQL)

This repository contains the corrected final submission for the E-commerce API assignment using Flask, SQLAlchemy, Marshmallow, and MySQL.

## Submission status
This version includes the required assignment fixes:
- `User.address` field added
- `Product.productname` field implemented
- `Order.orderdate` field added
- Required order-related endpoints implemented
- Marshmallow `session=db.session` handling corrected
- Postman collection updated and verified

## Features
- User CRUD
- Product CRUD
- Order CRUD
- Order-product relationship management
- User-to-order and order-to-product relationships
- Input validation and serialization with Marshmallow
- JSON-based API responses with error handling

## Project structure
- `run.py` - starts the Flask application
- `init_db.py` - creates the database tables
- `config.py` - application configuration and MySQL connection settings
- `app/models.py` - SQLAlchemy ORM models and relationships
- `app/schemas.py` - Marshmallow validation and serialization
- `app/routes/users.py` - user endpoints
- `app/routes/products.py` - product endpoints
- `app/routes/orders.py` - order endpoints and order-product routes
- `Ecommerce_API_Postman_Collection.json` - Postman collection for testing
- `SUBMISSION_CHECKLIST.md` - final teacher-ready checklist

## Setup

### 1) Create MySQL database
Run this in MySQL:

```sql
CREATE DATABASE ecommerce_api;
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Configure environment variables
Create a `.env` file in the project root based on `.env.example`:

```env
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DB=ecommerce_api
```

### 4) Create tables

```bash
python init_db.py
```

### 5) Run the API

```bash
python run.py
```

Base URL:

```text
http://127.0.0.1:5000
```

## API endpoints

### Users
- `POST /users`
- `GET /users`
- `GET /users/<user_id>`
- `PUT /users/<user_id>`
- `DELETE /users/<user_id>`

Example create user payload:

```json
{
  "name": "Alice Johnson",
  "email": "alice@example.com",
  "address": "123 Main Street"
}
```

### Products
- `POST /products`
- `GET /products`
- `GET /products/<product_id>`
- `PUT /products/<product_id>`
- `DELETE /products/<product_id>`

Example create product payload:

```json
{
  "productname": "Mechanical Keyboard",
  "description": "RGB backlit mechanical keyboard",
  "price": 89.99,
  "stock_quantity": 25
}
```

### Orders
- `POST /orders`
- `GET /orders`
- `GET /orders/<order_id>`
- `PUT /orders/<order_id>`
- `DELETE /orders/<order_id>`
- `PUT /orders/<orderid>/addproduct/<product_id>`
- `DELETE /orders/<orderid>/removeproduct/<product_id>`
- `GET /orders/user/<user_id>`
- `GET /orders/<order_id>/products`

Example create order payload:

```json
{
  "user_id": 1,
  "product_ids": [1, 2],
  "status": "pending"
}
```

## Testing notes
The project has been tested with a fresh database reset and the required routes were verified successfully.

## Final note
This is the revised submission version for the assignment after the instructor feedback. The project has been updated to align with the assignment requirements and is ready for teacher review.
