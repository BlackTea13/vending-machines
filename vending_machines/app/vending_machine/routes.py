from flask import request, jsonify
from app.extensions import db,  Session
from app.models.vending_machine import Vending_Machine
from app.models.machine_stock import Machine_Stock
from app.models.product import Product
from app.vending_machine import bp


@bp.route('/vending-machine/all', methods=['GET'])
def get_all_vending_machines():
    vending_machines = Session().query(Vending_Machine).all()
    products = Session().query(Product).all()
    machine_stock = Session().query(Machine_Stock).all()
    return Vending_Machine.objects_to_dictionary(vending_machines, machine_stock, products)


@ bp.route('/vending-machine/<int:id>', methods=['GET'])
def get_vending_machine(id):
    m1 = Vending_Machine(location="my house")
    a = jsonify(m1)
    print(a)
    return "you just accessed a vending machine route :)"


@ bp.route('/vending-machine/create/', methods=['GET'])
def create_vending_machine(id, location):
    request.args.get
