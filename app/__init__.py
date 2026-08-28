from flask import Flask, jsonify
from marshmallow import ValidationError
from dotenv import load_dotenv
from sqlalchemy.exc import IntegrityError

from app.extensions import db, ma
from app.routes.orders import orders_bp
from app.routes.products import products_bp
from app.routes.users import users_bp
from config import Config


def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    ma.init_app(app)

    app.register_blueprint(users_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(orders_bp)

    @app.route("/")
    def health_check():
        return jsonify({"message": "E-commerce API is running"}), 200

    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        return jsonify({"errors": error.messages}), 400

    @app.errorhandler(404)
    def handle_not_found(error):
        return jsonify({"error": "The requested resource was not found."}), 404

    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        return jsonify({"error": "Method not allowed on this endpoint."}), 405

    @app.errorhandler(IntegrityError)
    def handle_integrity_error(error):
        db.session.rollback()
        return jsonify({"error": str(error.orig)}), 400

    return app
