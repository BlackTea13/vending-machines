from __future__ import annotations
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.extensions import Base
from app.models import vending_machine
from app.models.product import Product
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

    product_info: Product = relationship("Product", foreign_keys=[product_id])

    def to_dict(self) -> dict:

        return {
            "product_id": self.product_id,
            "product_name": self.product_info.product_name,
            "product_price": self.product_info.price,
            "quantity": self.quantity,
        }
