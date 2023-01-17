from app.main import bp


@bp.route('/')
def index():
    return "welcome to Mr.Blum's vending machine tracking API! :)"