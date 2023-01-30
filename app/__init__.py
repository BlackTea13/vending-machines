from flask import Flask
from app.extensions import db, Base, Engine, Session
from app.models.vending_machine import VendingMachine
from app.models.product import Product
from app.models.machine_stock import MachineStock
from config import Config
import sys

sys.path.append('../')


def drop_tables():
    session = Session()
    Base.metadata.drop_all()
    session.close()


def insert_sample_data():
    m1 = VendingMachine('front of school')
    m2 = VendingMachine('back of school')
    m3 = VendingMachine('my house')

    p1 = Product('coke', 20)
    p2 = Product('taro', 15)
    p3 = Product('chocolate', 50)
    p4 = Product('robert', 55.80)
    p5 = Product('nail clippers', 800.12345678)

    ms1 = MachineStock(1, 1, 50)
    ms2 = MachineStock(2, 3, 1)
    ms3 = MachineStock(3, 2, 2000)
    ms4 = MachineStock(1, 2, 2)

    session = Session()
    session.add(m1)
    session.add(m2)
    session.add(m3)
    session.add(p1)
    session.add(p2)
    session.add(p3)
    session.add(p4)
    session.add(p5)
    session.commit()

    session.add(ms1)
    session.add(ms2)
    session.add(ms3)
    session.add(ms4)
    session.commit()


def create_app(config_class=Config):
    app = Flask(__name__)
    # app.config.from_object(config_class)
    app.config.from_object(Config)
    # Initialize Flask extensions here
    db.init_app(app)

    # Drop and create tables to put in the database server
    app.app_context().push()
    Base.metadata.drop_all(Engine)
    Base.metadata.create_all(Engine)

    # Sample data to add in for testing
    # Comment out the line below for production
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

    @app.route('/')
    def index():
        return "welcome to the API! :)"

    print('DEBUG: app starting')
    return app
