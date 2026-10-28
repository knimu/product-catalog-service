from flask import Blueprint, jsonify, request, abort
from service.models import Product, Category

products_bp = Blueprint("products", __name__)

def _json_product(product):
    return jsonify(product.serialize())

@products_bp.get("/products")
def list_products():
    name = request.args.get("name")
    category = request.args.get("category")
    available = request.args.get("available")

    if name:
        products = Product.find_by_name(name)
    elif category:
        try:
            products = Product.find_by_category(Category[category.upper()])
        except KeyError:
            return jsonify({"error": f"Unknown category: {category}"}), 400
    elif available is not None:
        products = Product.find_by_availability(available.lower() in ("true", "yes", "1"))
    else:
        products = Product.all()
    return jsonify([p.serialize() for p in products]), 200

@products_bp.post("/products")
def create_product():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "JSON body required"}), 400
    try:
        product = Product(name="")
        product.deserialize(data)
        product.create()
    except (ValueError, KeyError, TypeError) as exc:
        return jsonify({"error": str(exc)}), 400
    return jsonify(product.serialize()), 201

@products_bp.get("/products/<int:product_id>")
def read_product(product_id):
    product = Product.find(product_id)
    if product is None:
        abort(404, description=f"Product with id '{product_id}' was not found.")
    return _json_product(product), 200

@products_bp.put("/products/<int:product_id>")
def update_product(product_id):
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 415
    product = Product.find(product_id)
    if product is None:
        abort(404, description=f"Product with id '{product_id}' was not found.")
    data = request.get_json(silent=True) or {}
    try:
        product.deserialize(data)
        product.update()
    except (ValueError, KeyError, TypeError) as exc:
        return jsonify({"error": str(exc)}), 400
    return jsonify(product.serialize()), 200

@products_bp.delete("/products/<int:product_id>")
def delete_product(product_id):
    product = Product.find(product_id)
    if product is None:
        abort(404, description=f"Product with id '{product_id}' was not found.")
    product.delete()
    return "", 204
