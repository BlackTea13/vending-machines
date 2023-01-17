from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import Config
from app.extensions import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)

    # Register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.vending_machine import bp as vending_machine_bp
    app.register_blueprint(vending_machine_bp)

    from app.product import bp as product_bp
    app.register_blueprint(product_bp)
    
    from app.machine_stock import bp as machine_stock_bp
    app.register_blueprint(machine_stock_bp)

    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app