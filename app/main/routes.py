from flask import Response, jsonify

from app.main import bp


@bp.route("/")
def index() -> Response:
    return jsonify("welcome to Mr.Blum's vending machine tracking API! :)")
