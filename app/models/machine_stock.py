from __future__ import annotations
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.extensions import Base, Engine, Session, db
from app.models import vending_machine
from app.models import product
from dataclasses import dataclass


@dataclass
class MachineStock(Base):
    machine_id: int
    product_id: int
    quantity: int

    __tablename__ = 'machine_stock'
    machine_id = Column(Integer, ForeignKey(
        'vending_machines.machine_id'), primary_key=True)
    product_id = Column(Integer, ForeignKey(
        'products.product_id'), primary_key=True)
    quantity = Column(Integer)

    child: product.Product = relationship("Product", back_populates="parents",
                                          foreign_keys=[product_id])
    parent: vending_machine.VendingMachine = relationship(
        "VendingMachine", back_populates="children", foreign_keys=[machine_id])

    def __init__(self, machine_id: int, product_id: int, quantity: int):
        self.quantity = quantity
        self.machine_id = machine_id
        self.product_id = product_id
