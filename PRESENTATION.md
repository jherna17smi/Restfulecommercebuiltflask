# 5-Minute Presentation Script — E-commerce API

Total time: ~5 minutes (≈1.5 min / 1.5 min / 2 min)

---

## 1. What the project does (≈1.5 min)

"This project is a RESTful e-commerce API built with Flask, Flask-SQLAlchemy, Flask-Marshmallow, and MySQL.

It solves the core problem every e-commerce backend needs to solve: managing **users**, **products**, and **orders**, and correctly modeling how they relate to each other.

Specifically, it supports:
- Creating, reading, updating, and deleting **Users**
- Creating, reading, updating, and deleting **Products**
- Creating, reading, updating, and deleting **Orders**
- A **User can place many Orders** (one-to-many relationship)
- An **Order can contain many Products, and a Product can belong to many Orders** (many-to-many relationship)

This mirrors a real online store: a customer account, a product catalog, and a shopping order that ties them together."

---

## 2. How it works (≈1.5 min)

"At a high level, the project has four layers:

1. **Models** (`app/models.py`) — SQLAlchemy defines the `User`, `Product`, and `Order` tables, plus an association table called `order_products` that implements the many-to-many relationship between orders and products.

2. **Schemas** (`app/schemas.py`) — Marshmallow schemas validate incoming JSON (for example, requiring a valid email, or a positive price) and serialize database objects back into clean JSON responses, including nested data like an order's user and its list of products.

3. **Routes** (`app/routes/`) — Three Flask blueprints (`users`, `products`, `orders`) expose standard REST endpoints for each resource, following normal CRUD conventions: POST to create, GET to read, PUT to update, DELETE to remove.

4. **Database** — MySQL stores everything. When the server starts, `init_db.py` creates the tables directly from the SQLAlchemy models, so the database schema always matches the code.

The request flow is simple: Postman (or any client) sends a JSON request → Flask routes it to the right blueprint → Marshmallow validates it → SQLAlchemy reads/writes MySQL → Marshmallow serializes the response → Flask returns JSON."

---

## 3. Live demonstration (≈2 min)

Suggested demo order in Postman (use the included collection: `Ecommerce_API_Postman_Collection.json`):

1. **Health check**
   - `GET http://127.0.0.1:5000/`
   - Shows the API is running.

2. **Create a user**
   - `POST /users`
   ```json
   { "name": "Alice Johnson", "email": "alice@example.com" }
   ```
   - Point out: returns `201` with the new user's `id`.

3. **Create two products**
   - `POST /products`
   ```json
   { "name": "Mechanical Keyboard", "description": "RGB backlit", "price": 89.99, "stock_quantity": 25 }
   ```
   - `POST /products`
   ```json
   { "name": "Wireless Mouse", "description": "Ergonomic", "price": 24.99, "stock_quantity": 40 }
   ```

4. **Create an order linking the user to both products** (this is the many-to-many relationship in action)
   - `POST /orders`
   ```json
   { "user_id": 1, "product_ids": [1, 2] }
   ```

5. **Show the relationship result**
   - `GET /orders/1`
   - Point out in the response:
     - The nested `user` object (proves one-to-many: this order belongs to that user)
     - The `products` array with both items (proves many-to-many)
     - The computed `total_amount`

6. *(Optional, if time allows)* Show a validation error to prove input checking works:
   - `POST /users`
   ```json
   { "name": "X", "email": "not-an-email" }
   ```
   - Returns `400` with a clear validation message.

7. *(Optional)* Show it in MySQL Workbench:
   ```sql
   SELECT * FROM users;
   SELECT * FROM products;
   SELECT * FROM orders;
   SELECT * FROM order_products;
   ```
   - Point out `order_products` as the physical association table.

---

## Closing line

"This project demonstrates a complete, working REST API with proper relational modeling — a one-to-many relationship between users and orders, and a many-to-many relationship between orders and products — fully validated, serialized, and backed by a real MySQL database."
