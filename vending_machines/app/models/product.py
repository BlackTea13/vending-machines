from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.extensions import Base, Engine, Session, db

class Product(Base):
    __tablename__ = 'products'
    product_id = db.Column(Integer, primary_key=True, autoincrement=True)
    product_name = db.Column(String(1000))
    price = db.Column(Float)
        
    def __init__(self, product_name, price):
        product_name = product_name
        price = price
