from app import create_app
from app.extensions import db

app = create_app()
with app.app_context():
    db.drop_all()
    db.create_all()

    client = app.test_client()

    print('--- creating user ---')
    resp = client.post('/users', json={'name': 'Jose', 'email': 'jose@example.com', 'address': '123 Main St'})
    print(resp.status_code, resp.get_json())

    print('--- creating products ---')
    p1 = client.post('/products', json={'productname': 'Laptop', 'description': 'Gaming laptop', 'price': 999.99, 'stock_quantity': 5})
    print(p1.status_code, p1.get_json())
    p2 = client.post('/products', json={'name': 'Mouse', 'description': 'Wireless', 'price': 35.5, 'stock_quantity': 10})
    print(p2.status_code, p2.get_json())

    print('--- creating order ---')
    order_resp = client.post('/orders', json={'user_id': 1, 'product_ids': [1, 2], 'status': 'pending'})
    print(order_resp.status_code, order_resp.get_json())

    print('--- add product ---')
    add_resp = client.put('/orders/1/addproduct/2')
    print(add_resp.status_code, add_resp.get_json())

    print('--- remove product ---')
    rem_resp = client.delete('/orders/1/removeproduct/2')
    print(rem_resp.status_code, rem_resp.get_json())

    print('--- get orders by user ---')
    by_user = client.get('/orders/user/1')
    print(by_user.status_code, by_user.get_json())

    print('--- get order products ---')
    order_products = client.get('/orders/1/products')
    print(order_products.status_code, order_products.get_json())

    print('--- update user address ---')
    upd = client.put('/users/1', json={'address': '456 Elm Ave'})
    print(upd.status_code, upd.get_json())

    print('--- list all products ---')
    products = client.get('/products')
    print(products.status_code, products.get_json())

    print('VERIFICATION_COMPLETE')
