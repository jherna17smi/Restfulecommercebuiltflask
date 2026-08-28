from flask import Blueprint, jsonify, request

from app.extensions import db
from app.models import User
from app.schemas import user_schema, users_schema

users_bp = Blueprint("users", __name__, url_prefix="/users")


@users_bp.route("", methods=["POST"])
def create_user():
    payload = user_schema.load(request.get_json(force=True, silent=True) or {})

    existing_user = User.query.filter_by(email=payload.email).first()
    if existing_user:
        return jsonify({"error": "A user with this email already exists."}), 409

    db.session.add(payload)
    db.session.commit()
    return user_schema.jsonify(payload), 201


@users_bp.route("", methods=["GET"])
def list_users():
    users = User.query.order_by(User.id.asc()).all()
    return users_schema.jsonify(users), 200


@users_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return user_schema.jsonify(user), 200


@users_bp.route("/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    payload = user_schema.load(request.get_json(force=True, silent=True) or {}, partial=True)

    if payload.email and payload.email != user.email:
        email_taken = User.query.filter_by(email=payload.email).first()
        if email_taken:
            return jsonify({"error": "A user with this email already exists."}), 409

    if payload.name is not None:
        user.name = payload.name
    if payload.email is not None:
        user.email = payload.email

    db.session.commit()
    return user_schema.jsonify(user), 200


@users_bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": f"User {user_id} deleted successfully."}), 200
