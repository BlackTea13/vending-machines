from flask import request, redirect, url_for, jsonify, Response
from app.extensions import db,  Session
from app.models.vending_machine import Vending_Machine
from app.models.machine_stock import Machine_Stock
from app.models.product import Product
from app.product import bp

RESPONSE_CODE_BAD_REQUEST = 400

@bp.route('/product/all', methods=['GET'])
def get_all_products():
    products = Session().query(Product).all()
    return [Product.object_to_dictionary(product) for product in products]

@bp.route('/product/', methods=['GET'])
def get_product():
    if 'product_id' not in request.args and 'product_name' not in request.args:
        return 'product_id field and product_name field not in form...', RESPONSE_CODE_BAD_REQUEST
    
    product = None
    if 'product_id' in request.args:
        product_id = request.args.get('product_id')
        product = Session().query(Product).filter(Product.product_id == product_id).first()
        
    elif 'product_name' in request.args:
        product_name = request.args.get('product_name')
        product = Session().query(Product).filter(Product.product_name == product_name).first()
    
    if product == None:
        return f"product does not exist...", RESPONSE_CODE_BAD_REQUEST
    
    return Product.object_to_dictionary(product)

@bp.route('/product/create', methods=['POST'])
def create_product():
    form = request.form
    if 'product_name' not in form:
        return 'product name not in request body...', RESPONSE_CODE_BAD_REQUEST
    if 'price' not in form:
        return 'product price not in body...', RESPONSE_CODE_BAD_REQUEST
    
    new_product = Product(form.get('product_name'), form.get('price'))

    session = Session()
    session.add(new_product)
    session.commit()
    return redirect(url_for('.get_product', product_id=new_product.product_id))

@bp.route('/product/delete', methods=['POST'])
def delete_product():
    form = request.form
    if 'product_id' not in form:
        return 'product_id not in body', RESPONSE_CODE_BAD_REQUEST
    
    
    product_id = form.get('product_id')
    session = Session()
    product = session.query(Product).filter(
        Product.product_id == product_id).first()
    if product == None:
        return f'product with machine_id {product_id} does not exist...', RESPONSE_CODE_BAD_REQUEST

    session.delete(product)
    session.commit()
    session.close()
    return redirect(url_for(".get_all_products"))