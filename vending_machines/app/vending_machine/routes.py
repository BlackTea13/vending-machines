from flask import request, jsonify
from app.extensions import db
from app.models.vending_machine import Vending_Machine
from app.vending_machine import bp

@bp.route('/vending-machine/all', methods=['GET'])
def get_all_vending_machines():
    return 'all vending machines'

@bp.route('/vending-machine/<int:id>', methods=['GET'])
def get_vending_machine(id):    
    m1 = Vending_Machine(location="my house")
    a = jsonify(m1)
    print(a)
    return "you just accessed a vending machine route :)"