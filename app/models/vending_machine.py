from __future__ import annotations
from sqlalchemy import Column, Integer, String, MetaData
from sqlalchemy.orm import relationship
from app.extensions import Base, Engine, Session, db
from dataclasses import dataclass
from typing import List
from app.models import machine_stock
from app.models import product


@dataclass
class Vending_Machine(Base):
    machine_id: int
    location: str

    __tablename__ = 'vending_machines'
    machine_id = Column(Integer, primary_key=True,
                        autoincrement=True)
    location = Column(String(1000))
    children: List[machine_stock.Machine_Stock] = relationship(
        "Machine_Stock", back_populates="parent", cascade="all,delete")

    def __init__(self, location: str):
        self.location = location

    @staticmethod
    def get_product_id_in_object(vending_machine: Vending_Machine,
                                 machine_stocks: List[machine_stock.Machine_Stock]) -> List[int]:
        machine_id = vending_machine.machine_id
        product_ids = [
            listing.product_id for listing in machine_stocks if machine_id == listing.machine_id]
        return product_ids

    @staticmethod
    def object_to_dictionary(vending_machine: Vending_Machine):
        machine_dictionary = {'machine_id': vending_machine.machine_id, 'location': vending_machine.location}
        product_list = []
        for listing in vending_machine.children:
            product_dictionary = {'product_id': listing.child.product_id, 'product_name': listing.child.product_name,
                                  'price': listing.child.price, 'quantity': listing.quantity}
            product_list.append(product_dictionary)
        machine_dictionary['products'] = product_list
        return machine_dictionary

    # super cool method that was a waste of time
    @staticmethod
    def objects_to_dictionary(vending_machine: List[Vending_Machine], machine_stock: List[machine_stock.Machine_Stock], products: List[product.Product]) -> List[dict]:
        list_of_dictionary = []
        for machine in vending_machine:
            out_dictionary = {'machine_id': machine.machine_id, 'location': machine.location}

            from app.models.product import Product
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
