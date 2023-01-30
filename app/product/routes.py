from flask import request, jsonify, Response
from app.extensions import Session
from app.models.product import Product
from app.product import bp
from typing import Tuple
from http import HTTPStatus


@bp.route('/product/all', methods=['GET'])
def get_all_products() -> Response:
    with Session() as session:
        Response(status=HTTPStatus.NON_AUTHORITATIVE_INFORMATION)
        return jsonify(Product.get_all_products(session))


@bp.route('/product/', methods=['GET'])
def get_product() -> Response:
    if 'product_id' not in request.args and 'product_name' not in request.args:
        return Response(response="product_id or product_name not found", status=HTTPStatus.BAD_REQUEST)
    with Session() as session:
        if 'product_id' in request.args:
            result = Product.get_product_by_id(session, request.args.get('product_id'))
        elif 'product_name' in request.args:
            result = Product.get_product_by_name(session, request.args.get('product_name'))
    if result is None:
        return Response(response="product does not exist", status=HTTPStatus.NOT_FOUND)
    return jsonify(result)


@bp.route('/product/create', methods=['POST'])
def create_product() -> Response | Tuple[Response, int]:
    form = request.form
    if 'product_name' not in form.keys():
        return Response(response="product_name not in request body", status=HTTPStatus.BAD_REQUEST)
    if 'price' not in form.keys():
        return Response(response="product_id not in request body", status=HTTPStatus.BAD_REQUEST)

    with Session() as session:
        result = Product.create(session, form.get('product_name'), form.get('price'))
        if result.item is None:
            return Response(response=result.message, status=HTTPStatus.BAD_REQUEST)
        else:
            new_product = result.item
        session.add(new_product)
        session.commit()
    return jsonify(new_product), 203


@bp.route('/product/delete', methods=['POST'])
def delete_product() -> Response:
    form = request.form
    if 'product_id' not in form.keys():
        return Response(response="product_id not in request body", status=HTTPStatus.BAD_REQUEST)

    product_id = form.get('product_id')
    with Session() as session:
        result = Product.delete(session, product_id)
    if result.item is None:
        Response(response=result.message, status=HTTPStatus.NOT_FOUND)
    return Response(response=result.message, status=HTTPStatus.OK)
