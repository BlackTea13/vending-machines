from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from app.extensions import db


from sqlalchemy import Column, Integer, String, MetaData, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.extensions import Base, Engine, Session, db
from flask import jsonify
from dataclasses import dataclass
from typing import List

@dataclass
class Vending_Machine(Base):
    machine_id : int
    location : str
    
    __tablename__ = 'vending_machines'
    machine_id = db.Column(Integer, primary_key=True, autoincrement=True)
    location = db.Column(String(1000))
    
    children = relationship("Machine_Stock")
    
    def __init__(self, location):
        self.location = location
        
    @staticmethod
    def create_machine_by_id(id: int):
        pass


@dataclass
class Product(Base):
    __tablename__ = 'products'
    product_id = db.Column(Integer, primary_key=True, autoincrement=True)
    product_name = db.Column(String(1000))
    price = db.Column(Float)
        
    def __init__(self, product_name, price):
        product_name = product_name
        price = price

    
@dataclass
class Machine_Stock(Base):
    __tablename__ = 'machine_stock'
    machine_id = db.Column(Integer, ForeignKey('vending_machines.machine_id'), primary_key=True)
    product_id = db.Column(Integer, ForeignKey('products.product_id'), primary_key=True)
    quantity = db.Column(Integer)
    
    child = relationship("Product")
    
    def __init__(self, quantity):
        quantity = quantity
    
    def do_something():
        return None
        
    
def create_app(config_class=Config):
    app = Flask(__name__)
    #app.config.from_object(config_class)
    app.config.from_object(Config)
    # Initialize Flask extensions here
    db.init_app(app)
    
    with app.app_context():
        db.drop_all()
        db.create_all()
    
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