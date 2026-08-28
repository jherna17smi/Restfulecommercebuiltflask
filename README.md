# E-commerce API (Flask + MySQL)

This project is a fully functional e-commerce REST API built with:
- Flask
- Flask-SQLAlchemy
- Flask-Marshmallow
- MySQL

## Features

- Users CRUD
- Products CRUD
- Orders CRUD
- One-to-Many relationship: one user has many orders
- Many-to-Many relationship: orders contain many products, products can belong to many orders
- Input validation and serialization with Marshmallow

## Project Structure

- `run.py` - starts the Flask app
- `init_db.py` - creates database tables
- `config.py` - MySQL/Flask configuration
- `app/models.py` - SQLAlchemy models and relationships
- `app/schemas.py` - Marshmallow schemas
- `app/routes/users.py` - user endpoints
- `app/routes/products.py` - product endpoints
- `app/routes/orders.py` - order endpoints

## 1) Create MySQL Database

In MySQL Workbench, run:

```sql
CREATE DATABASE ecommerce_api;
```

Optional (if you want a dedicated DB user):

```sql
CREATE USER 'ecommerce_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON ecommerce_api.* TO 'ecommerce_user'@'localhost';
FLUSH PRIVILEGES;
```

## 2) Install Dependencies

```bash
pip install -r requirements.txt
```

## 3) Configure Environment Variables

Copy `.env.example` to `.env` and set your values.

Example:

```env
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DB=ecommerce_api
```

## 4) Create Tables

```bash
python init_db.py
```

## 5) Run API

```bash
python run.py
```

Base URL:

```text
http://127.0.0.1:5000
```

## API Endpoints

### Users
- `POST /users`
- `GET /users`
- `GET /users/<user_id>`
- `PUT /users/<user_id>`
- `DELETE /users/<user_id>`

Example body (`POST /users`):

```json
{
  "name": "Alice Johnson",
  "email": "alice@example.com"
}
```

### Products
- `POST /products`
- `GET /products`
- `GET /products/<product_id>`
- `PUT /products/<product_id>`
- `DELETE /products/<product_id>`

Example body (`POST /products`):

```json
{
  "name": "Keyboard",
  "description": "Mechanical keyboard",
  "price": 89.99,
  "stock_quantity": 20
}
```

### Orders
- `POST /orders`
- `GET /orders`
- `GET /orders/<order_id>`
- `PUT /orders/<order_id>`
- `DELETE /orders/<order_id>`

Example body (`POST /orders`):

```json
{
  "user_id": 1,
  "product_ids": [1, 2],
  "status": "pending"
}
```

## Postman Test Flow

1. Create at least one user with `POST /users`.
2. Create at least two products with `POST /products`.
3. Create an order with `POST /orders` using valid `user_id` and `product_ids`.
4. Verify relationships using `GET /orders` and `GET /orders/<id>`.
5. Update and delete records to validate all CRUD operations.

## Notes

- If MySQL connection fails, verify host, port, username, and password in `.env`.
- If you update model definitions, re-run `python init_db.py` (or use migrations in future enhancements).
