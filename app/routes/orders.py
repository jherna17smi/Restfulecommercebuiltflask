from flask import Blueprint, jsonify, request

from app.extensions import db
from app.models import Order, Product, User
from app.schemas import order_response_schema, order_write_schema, orders_response_schema

orders_bp = Blueprint("orders", __name__, url_prefix="/orders")


def _resolve_products(product_ids):
    products = Product.query.filter(Product.id.in_(product_ids)).all()
    found_ids = {product.id for product in products}
    missing_ids = sorted(list(set(product_ids) - found_ids))
    return products, missing_ids


@orders_bp.route("", methods=["POST"])
def create_order():
    payload = order_write_schema.load(request.get_json(force=True, silent=True) or {})

    user = User.query.get_or_404(payload["user_id"])
    products, missing_ids = _resolve_products(payload["product_ids"])

    if missing_ids:
        return (
            jsonify({"error": "Some product IDs do not exist.", "missing_ids": missing_ids}),
            400,
        )

    order = Order(user_id=user.id, status=payload["status"])
    order.products = products

    db.session.add(order)
    db.session.commit()

    return order_response_schema.jsonify(order), 201


@orders_bp.route("", methods=["GET"])
def list_orders():
    orders = Order.query.order_by(Order.id.asc()).all()
    return orders_response_schema.jsonify(orders), 200


@orders_bp.route("/<int:order_id>", methods=["GET"])
def get_order(order_id):
    order = Order.query.get_or_404(order_id)
    return order_response_schema.jsonify(order), 200


@orders_bp.route("/<int:order_id>", methods=["PUT"])
def update_order(order_id):
    order = Order.query.get_or_404(order_id)
    payload = order_write_schema.load(request.get_json(force=True, silent=True) or {}, partial=True)

    if "user_id" in payload:
        user = User.query.get_or_404(payload["user_id"])
        order.user_id = user.id

    if "status" in payload:
        order.status = payload["status"]

    if "product_ids" in payload:
        products, missing_ids = _resolve_products(payload["product_ids"])
        if missing_ids:
            return (
                jsonify({
                    "error": "Some product IDs do not exist.",
                    "missing_ids": missing_ids,
                }),
                400,
            )
        order.products = products

    db.session.commit()
    return order_response_schema.jsonify(order), 200


@orders_bp.route("/<int:order_id>", methods=["DELETE"])
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    return jsonify({"message": f"Order {order_id} deleted successfully."}), 200
