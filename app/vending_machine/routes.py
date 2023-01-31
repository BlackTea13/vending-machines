from flask import request, redirect, url_for, Response, jsonify
from app.extensions import Session
from app.models.vending_machine import VendingMachine
from app.models.machine_stock import MachineStock
from app.models.product import Product
from app.vending_machine import bp
from app.utils.result import Result
from typing import Dict, List, Tuple, Union
from http import HTTPStatus


@bp.route('/vending-machine/all', methods=['GET'])
def get_all_vending_machines() -> Response:
    with Session() as session:
        return jsonify(VendingMachine.get_all_vending_machines(session))


@bp.route('/vending-machine/', methods=['GET'])
def get_vending_machine() -> Response:
    if 'machine_id' not in request.args and 'location' not in request.args:
        return Response(response="machine_id or location not in request arguments", status=HTTPStatus.BAD_REQUEST)
    with Session() as session:
        if 'machine_id' in request.args:
            result = VendingMachine.get_vending_machine_by_id(session, request.args.get('machine_id'))
        elif 'location' in request.args:
            result = VendingMachine.get_vending_machine_by_location(session, request.args.get('location'))
        if result is None:
            return Response(response="machine does not exist", status=HTTPStatus.NOT_FOUND)
        return jsonify(result)


@bp.route('/vending-machine/create/', methods=['POST'])
def create_vending_machine() -> Response:
    form = request.form
    if 'location' not in form:
        return Response(response='location for vending machine not in request body...',
                        status=HTTPStatus.BAD_REQUEST)
    with Session() as session:
        result: Result = VendingMachine.create(session, form['location'])
        if result is None:
            return Response(response=result.message, status=HTTPStatus.BAD_REQUEST)
        session.add(result.item)
        session.commit()
    return Response(response='vending machine created', status=HTTPStatus.CREATED)


@bp.route('/vending-machine/delete/', methods=['POST'])
def delete_vending_machine() -> Union[Response, redirect]:
    form = request.form
    if 'machine_id' not in form:
        return Response(response='machine_id field not in form...', status=HTTPStatus.BAD_REQUEST)

    machine_id = form.get('machine_id')
    with Session() as session:
        result = VendingMachine.delete_machine_by_id(session, machine_id)
    if result.item is None:
        return Response(response=result.message, status=HTTPStatus.BAD_REQUEST)
    return Response(response=result.message, status=HTTPStatus.OK)


@bp.route('/vending-machine/add-product/', methods=['POST'])
def add_product_to_machine() -> Response:
    form = request.form
    if 'machine_id' not in form or not form.get('machine_id').isdecimal():
        return Response(response='machine_id field not in form...', status=HTTPStatus.BAD_REQUEST)
    if 'product_id' not in form or not form.get('product_id').isdecimal():
        return Response(response='product_id field not in form...', status=HTTPStatus.BAD_REQUEST)
    if 'quantity' not in form or not form.get('quantity').isdecimal():
        return Response(response='quantity field not in form...', status=HTTPStatus.BAD_REQUEST)

    machine_id = form.get('machine_id')
    quantity = form.get('quantity')
    product_id = form.get('product_id')
    with Session() as session:
        machine = VendingMachine.get_vending_machine_by_id(session, machine_id)
        if machine is None:
            return Response(response='machine not found', status=HTTPStatus.NOT_FOUND)
        result = machine.add_product_by_id(session, product_id, quantity)
    if result.item is None:
        return Response(response=result.message, status=HTTPStatus.BAD_REQUEST)
    return Response(response=result.message, status=HTTPStatus.OK)


@bp.route('/vending-machine/edit-product/', methods=['POST'])
def edit_product_quantity_in_machine() -> Response:
    form = request.form
    if 'machine_id' not in form:
        return Response(response='machine_id field not in form...', status=HTTPStatus.BAD_REQUEST)
    if 'product_id' not in form:
        return Response(response='product_id field not in form...', status=HTTPStatus.BAD_REQUEST)
    if 'quantity' not in form:
        return Response(response='quantity field not in form...', status=HTTPStatus.BAD_REQUEST)

    machine_id = form.get('machine_id')
    quantity = form.get('quantity')
    product_id = form.get('product_id')
    with Session() as session:
        machine = VendingMachine.get_vending_machine_by_id(session, machine_id)
        if machine is None:
            return Response(response='machine not found', status=HTTPStatus.NOT_FOUND)
        result = machine.increase_product_quantity_by_id(session, product_id, quantity)
    if result.item is None:
        return Response(response=result.message, status=HTTPStatus.BAD_REQUEST)
    return Response(response=result.message, status=HTTPStatus.OK)

