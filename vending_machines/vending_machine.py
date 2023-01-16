from flask import Blueprint

vending_machine = Blueprint("vending_machine", __name__)

@vending_machine.route('/vending-machine/<int:id>')
def get_vending_machine():
    return "this is a vending machine"