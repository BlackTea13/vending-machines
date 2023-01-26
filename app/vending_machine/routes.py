from flask import request, redirect, url_for, jsonify, Response
from app.extensions import db,  Session
from app.models.vending_machine import VendingMachine
from app.models.machine_stock import MachineStock
from app.models.product import Product
from app.vending_machine import bp

RESPONSE_CODE_BAD_REQUEST = 400
RESPONSE_CODE_CREATED = 201


@bp.route('/vending-machine/all', methods=['GET'])
def get_all_vending_machines():
    vending_machines = Session().query(VendingMachine).all()
    return [VendingMachine.object_to_dictionary(machine) for machine in vending_machines]


@bp.route('/vending-machine/', methods=['GET'])
def get_vending_machine():
    if request.method == 'GET':
        if 'location' not in request.args and 'machine_id' not in request.args:
            return f"location or machine_id information not in request", RESPONSE_CODE_BAD_REQUEST

        machine = None
        if 'location' in request.args:
            machine_location = request.args.get('location')
            machine = Session().query(VendingMachine).filter(
                VendingMachine.location == machine_location).first()

        elif 'machine_id' in request.args:
            machine_id = request.args.get('machine_id')
            machine = Session().query(VendingMachine).filter(
                VendingMachine.machine_id == machine_id).first()

        if machine == None:
            return f'machine with location: {machine_location} does not exist...', RESPONSE_CODE_BAD_REQUEST
        return VendingMachine.object_to_dictionary(machine)


@bp.route('/vending-machine/create/', methods=['POST'])
def create_vending_machine():
    form = request.form
    if 'location' not in form:
        return 'location for vending machine not in request body...', RESPONSE_CODE_BAD_REQUEST

    new_machine = VendingMachine(form['location'])

    session = Session()
    session.add(new_machine)
    session.commit()
    return redirect(url_for('.get_vending_machine', machine_id=new_machine.machine_id))


@bp.route('/vending-machine/delete/', methods=['POST'])
def delete_vending_machine():
    form = request.form
    if 'machine_id' not in form:
        return 'machine_id field not in form...', RESPONSE_CODE_BAD_REQUEST

    machine_id = form.get('machine_id')
    session = Session()
    machine = session.query(VendingMachine).filter(
        VendingMachine.machine_id == machine_id).first()
    if machine == None:
        return f'machine with machine_id {machine_id} does not exist...', RESPONSE_CODE_BAD_REQUEST

    session.delete(machine)
    session.commit()
    session.close()
    return redirect(url_for(".get_all_vending_machines"))


@bp.route('/vending-machine/add-product/', methods=['POST'])
def add_product_to_machine():
    form = request.form
    if 'machine_id' not in form:
        return 'machine_id field not in form...', RESPONSE_CODE_BAD_REQUEST
    if 'product_id' not in form:
        return 'product_id field not in form...', RESPONSE_CODE_BAD_REQUEST
    if 'quantity' not in form:
        return 'quantity field not in form...', RESPONSE_CODE_BAD_REQUEST

    quantity = form.get('quantity')
    product_id = form.get('product_id')
    session = Session()
    product = session.query(Product).filter(
        Product.product_id == product_id).first()

    if product == None:
        return f'product with id {product_id} does not exist in database...', RESPONSE_CODE_BAD_REQUEST

    machine_id = form.get('machine_id')
    machine = session.query(VendingMachine).filter(
        VendingMachine.machine_id == machine_id).first()

    if machine == None:
        return f'vending machine with id {machine_id} does not exist in database...', RESPONSE_CODE_BAD_REQUEST

    listing = MachineStock(machine_id, product_id, quantity)
    session.add(listing)
    session.commit()
    session.close()

    return redirect(url_for('.get_vending_machine', machine_id=machine_id))
