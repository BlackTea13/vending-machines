from __future__ import annotations
from sqlalchemy import Column, Integer, String, MetaData
from sqlalchemy.orm import relationship
from app.extensions import Base, Engine, Session, db
from flask import jsonify
from dataclasses import dataclass
from typing import List
from app.models.product import Product
from app.models.machine_stock import Machine_Stock


@dataclass
class Vending_Machine(Base):
    machine_id: int
    location: str

    __tablename__ = 'vending_machines'
    machine_id = Column(Integer, primary_key=True,
                        autoincrement=True)
    location = Column(String(1000))

    children = relationship("Machine_Stock", back_populates="parent")

    def __init__(self, location):
        self.location = location

    @staticmethod
    def get_product_id_in_object(vending_machine: Vending_Machine, machine_stocks: List[Machine_Stock]) -> dict:
        machine_id = vending_machine.machine_id
        product_ids = [
            listing.product_id for listing in machine_stocks if machine_id == listing.machine_id]
        return product_ids

    @staticmethod
    def objects_to_dictionary(vending_machine: List[Vending_Machine], machine_stock: List[Machine_Stock], products: List[Product]) -> List[dict]:
        list_of_dictionary = []
        for machine in vending_machine:
            out_dictionary = {}
            out_dictionary['machine_id'] = machine.machine_id
            out_dictionary['location'] = machine.location

            product_list = []
            for listing in machine_stock:
                product_dictionary = {}
                if listing.machine_id == machine.machine_id:
                    product = Product.get_product_by_id(
                        listing.product_id, products)
                    product_dictionary['product_id'] = listing.product_id
                    product_dictionary['product_name'] = product.product_name
                    product_dictionary['price'] = product.price
                    product_dictionary['quantity'] = listing.quantity
                    product_list.append(product_dictionary)

            out_dictionary['products'] = product_list
            list_of_dictionary.append(out_dictionary)
        return list_of_dictionary
