from flask import render_template, request, redirect, url_for
from app.products import products_bp

products = [
    {"id": 1, "name": "Watch", "price": 100.00},
    {"id": 2, "name": "Horse", "price": 399.99},
    {"id": 3, "name": "Gypsi", "price": 0.99},
]

@products_bp.route("/")
def list_products():
    """Список продуктів"""
    # БЕЗ префікса 'products/'
    return render_template("list.html", products=products)

@products_bp.route("/<int:product_id>")
def product_detail(product_id):
    """Деталі продукту"""
    product = next((p for p in products if p["id"] == product_id), None)
    if not product:
        return "Product not found", 404
    # БЕЗ префікса 'products/'
    return render_template("detail.html", product=product)

@products_bp.route("/api/<int:product_id>")
def product_api(product_id):
    """API для продукту"""
    product = next((p for p in products if p["id"] == product_id), None)
    if not product:
        return {"error": "Product not found"}, 404
    return product
