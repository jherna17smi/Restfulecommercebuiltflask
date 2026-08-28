from flask import Blueprint, jsonify, request

from app.extensions import db
from app.models import Product
from app.schemas import product_schema, products_schema

products_bp = Blueprint("products", __name__, url_prefix="/products")


@products_bp.route("", methods=["POST"])
def create_product():
    payload = product_schema.load(request.get_json(force=True, silent=True) or {})
    db.session.add(payload)
    db.session.commit()
    return product_schema.jsonify(payload), 201


@products_bp.route("", methods=["GET"])
def list_products():
    products = Product.query.order_by(Product.id.asc()).all()
    return products_schema.jsonify(products), 200


@products_bp.route("/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return product_schema.jsonify(product), 200


@products_bp.route("/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    payload = product_schema.load(request.get_json(force=True, silent=True) or {}, partial=True)

    if payload.name is not None:
        product.name = payload.name
    if payload.description is not None:
        product.description = payload.description
    if payload.price is not None:
        product.price = payload.price
    if payload.stock_quantity is not None:
        product.stock_quantity = payload.stock_quantity

    db.session.commit()
    return product_schema.jsonify(product), 200


@products_bp.route("/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": f"Product {product_id} deleted successfully."}), 200
