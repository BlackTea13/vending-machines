from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.extensions import db, Base, Engine, Session
from app.models.vending_machine import Vending_Machine
from app.models.product import Product
from app.models.machine_stock import Machine_Stock
from config import Config
import sys
sys.path.append('../')


def drop_tables():
    session = Session()
    Base.metadata.drop_all()


def insert_sample_data():
    m1 = Vending_Machine('front of school')
    m2 = Vending_Machine('back of school')
    m3 = Vending_Machine('my house')

    p1 = Product('coke', 20)
    p2 = Product('taro', 15)
    p3 = Product('chocolate', 50)

    ms1 = Machine_Stock(1, 1, 50)
    ms2 = Machine_Stock(2, 3, 1)
    ms3 = Machine_Stock(3, 2, 2000)

    session = Session()
    session.add(m1)
    session.add(m2)
    session.add(m3)
    session.add(p1)
    session.add(p2)
    session.add(p3)
    session.commit()

    session.add(ms1)
    session.add(ms2)
    session.add(ms3)
    session.commit()


def create_app(config_class=Config):
    app = Flask(__name__)
    # app.config.from_object(config_class)
    app.config.from_object(Config)
    # Initialize Flask extensions here
    db.init_app(app)

    app.app_context().push()
    Base.metadata.drop_all(Engine)
    Base.metadata.create_all(Engine)
    insert_sample_data()

    # Register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.machine_stock import bp as machine_stock_bp
    app.register_blueprint(machine_stock_bp)

    from app.vending_machine import bp as vending_machine_bp
    app.register_blueprint(vending_machine_bp)

    from app.product import bp as product_bp
    app.register_blueprint(product_bp)

    print('DEBUG: app starting')
    return app
