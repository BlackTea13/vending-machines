from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.extensions import Base, Engine, Session


class Machine_Stock(Base):
    __tablename__ = 'machine_stock'
    machine_id = Column(Integer, ForeignKey('vending_machines.machine_id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('products.product_id'), primary_key=True)
    quantity = Column(Integer)
    
    child = relationship("Product")
    
    def __init__(self, quantity):
        quantity = quantity
    
    def do_something():
        return None
        
    
    
    