from flask import jsonify, request
from vending_machine import vending_machine

@vending_machine.route('/vending-machine/<int:id>')
def get_vending_machine():
    return "this is a vending machine"