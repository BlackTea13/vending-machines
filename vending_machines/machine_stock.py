from flask import Blueprint

machine_stock = Blueprint("machine_stock", __name__)

@machine_stock.route('/vending-machine/<int:id>/stock')
def get_vending_machine():
    return "this is a listing in a certain vending machine"