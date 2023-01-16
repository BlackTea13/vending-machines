from flask import Blueprint

product = Blueprint("product", __name__)

@product.route('/product/<int:id>')
def get_product(id: int):
    return f"id: {id}"