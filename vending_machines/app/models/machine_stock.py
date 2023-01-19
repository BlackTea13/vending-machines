from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.extensions import Base, Engine, Session, db
from dataclasses import dataclass


@dataclass
class Machine_Stock(Base):
    machine_id: int
    product_id: int
    quantity: int

    __tablename__ = 'machine_stock'
    machine_id = Column(Integer, ForeignKey(
        'vending_machines.machine_id'), primary_key=True)
    product_id = Column(Integer, ForeignKey(
        'products.product_id'), primary_key=True)
    quantity = Column(Integer)

    child = relationship("Product", back_populates="parents",
                         foreign_keys=[product_id])
    parent = relationship(
        "Vending_Machine", back_populates="children", foreign_keys=[machine_id])

    def __init__(self, machine_id, product_id, quantity):
        self.quantity = quantity
        self.machine_id = machine_id
        self.product_id = product_id

    def do_something():
        return None
