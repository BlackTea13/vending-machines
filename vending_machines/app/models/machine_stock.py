from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.extensions import Base, Engine, Session, db


class Machine_Stock(Base):
    __tablename__ = 'machine_stock'
    machine_id = Column(Integer, ForeignKey(
        'vending_machines.machine_id'), primary_key=True)
    product_id = Column(Integer, ForeignKey(
        'products.product_id'), primary_key=True)
    quantity = Column(Integer)

    child = relationship("Product")

    def __init__(self, machine_id, product_id, quantity):
        self.quantity = quantity
        self.machine_id = machine_id
        self.product_id = product_id

    def do_something():
        return None
