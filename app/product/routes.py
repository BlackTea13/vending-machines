from http import HTTPStatus
from typing import Tuple

from flask import Response, jsonify, request

from app.extensions import Session
from app.models import stock_timeline
from app.models.product import Product
from app.product import bp


@bp.route("/product/all", methods=["GET"])
def get_all_products() -> Response:
    with Session() as session:
        return jsonify(Product.get_all_products(session))


@bp.route("/product/", methods=["GET"])
def get_product() -> Response:
    if "product_id" not in request.args and "product_name" not in request.args:
        return Response(
            response="product_id or product_name not found",
            status=HTTPStatus.BAD_REQUEST,
        )
    with Session() as session:
        if "product_id" in request.args:
            result = Product.get_product_by_id(session, request.args.get("product_id"))
        elif "product_name" in request.args:
            result = Product.get_product_by_name(session, request.args.get("product_name"))
    if result is None:
        return Response(response="product does not exist", status=HTTPStatus.NOT_FOUND)
    return jsonify(result)


@bp.route("/product/create", methods=["POST"])
def create_product() -> Response | Tuple[Response, int]:
    form = request.form
    if "product_name" not in form:
        return Response(response="product_name not in request body", status=HTTPStatus.BAD_REQUEST)
    if "price" not in form.keys():
        return Response(response="product_id not in request body", status=HTTPStatus.BAD_REQUEST)

    with Session() as session:
        result = Product.create(session, form.get("product_name"), form.get("price"))
        if result.item is None:
            return Response(response=result.message, status=HTTPStatus.BAD_REQUEST)
        session.add(result.item)
        session.commit()
    return jsonify(result.item), 201


@bp.route("/product/edit", methods=["POST"])
def edit_product() -> Response | tuple[Response, int]:
    form = request.form
    if "product_id" not in form.keys():
        return Response(response="product_id not in request body", status=HTTPStatus.BAD_REQUEST)
    with Session() as session:
        price = form.get("price") if "price" in form.keys() else None
        product_name = form.get("product_name") if "product_name" in form.keys() else None
        product_to_edit = Product.get_product_by_id(session, form.get("product_id"))
        if product_to_edit is None:
            return Response(response="product does not exist", status=HTTPStatus.BAD_REQUEST)
        result = product_to_edit.edit(session=session, product_name=product_name, price=price)
    if result.item is None:
        return Response(response=result.message, status=HTTPStatus.BAD_REQUEST)
    return jsonify(result.item), 200


@bp.route("/product/delete", methods=["POST"])
def delete_product() -> Response:
    form = request.form
    if "product_id" not in form.keys():
        return Response(response="product_id not in request body", status=HTTPStatus.BAD_REQUEST)

    product_id = form.get("product_id")
    with Session() as session:
        result = Product.delete(session, product_id)
    if result.item is None:
        return Response(response=result.message, status=HTTPStatus.BAD_REQUEST)
    return Response(response=result.message, status=HTTPStatus.OK)


@bp.route("/product/records", methods=["POST"])
def product_record() -> Response:
    form = request.form
    if "product_id" not in form.keys():
        return Response(response="product_id not in request body", status=HTTPStatus.BAD_REQUEST)
    product_id = form.get("product_id")

    result = stock_timeline.StockTimeline.product_time_stamp_in_records(product_id)
    return jsonify(result)
