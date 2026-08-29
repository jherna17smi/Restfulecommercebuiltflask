from marshmallow import Schema, ValidationError, fields, validate, validates

from app.extensions import ma
from app.models import Order, Product, User


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        include_fk = True
        include_relationships = True

    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=2, max=120))
    email = fields.Email(required=True)
    address = fields.String(required=True, validate=validate.Length(min=2, max=255))
    created_at = fields.DateTime(dump_only=True)


class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        load_instance = True
        include_fk = True
        include_relationships = True

    id = fields.Integer(dump_only=True)
    productname = fields.String(required=True, validate=validate.Length(min=2, max=120))
    description = fields.String(allow_none=True)
    price = fields.Float(required=True, validate=validate.Range(min=0))
    stock_quantity = fields.Integer(required=True, validate=validate.Range(min=0))
    created_at = fields.DateTime(dump_only=True)


class OrderWriteSchema(Schema):
    user_id = fields.Integer(required=True, strict=True)
    product_ids = fields.List(
        fields.Integer(strict=True),
        required=True,
        validate=validate.Length(min=1),
    )
    status = fields.String(
        load_default="pending",
        validate=validate.OneOf(["pending", "paid", "shipped", "cancelled"]),
    )

    @validates("product_ids")
    def validate_unique_products(self, value, **kwargs):
        if len(value) != len(set(value)):
            raise ValidationError("product_ids must not contain duplicates.")


class OrderResponseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        load_instance = True
        include_fk = True
        include_relationships = True

    id = fields.Integer(dump_only=True)
    status = fields.String()
    orderdate = fields.DateTime(dump_only=True)
    created_at = fields.DateTime(dump_only=True, attribute="orderdate")
    user = fields.Nested(UserSchema(only=("id", "name", "email", "address")))
    products = fields.List(
        fields.Nested(ProductSchema(only=("id", "productname", "price", "stock_quantity")))
    )
    total_amount = fields.Method("get_total_amount")

    def get_total_amount(self, obj):
        return round(sum(product.price for product in obj.products), 2)


user_schema = UserSchema()
users_schema = UserSchema(many=True)

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

order_write_schema = OrderWriteSchema()
orders_write_schema = OrderWriteSchema(many=True)

order_response_schema = OrderResponseSchema()
orders_response_schema = OrderResponseSchema(many=True)
