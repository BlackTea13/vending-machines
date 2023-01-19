from __future__ import annotations
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.extensions import Base, Engine, Session, db
from dataclasses import dataclass
from typing import List


@dataclass
class Product(Base):
    product_id: int
    product_name: str
    price: float

    __tablename__ = 'products'
    product_id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String(1000))
    price = Column(Float)

    parents = relationship("Machine_Stock", back_populates="child")

    def __init__(self, product_name, price):
        self.product_name = product_name
        self.price = price

    @staticmethod
    def get_product_by_id(id: int, products: List[Product]) -> Product:
        for product in products:
            if product.product_id == id:
                return product
        return None
