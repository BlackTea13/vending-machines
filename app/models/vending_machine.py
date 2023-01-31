from __future__ import annotations

from typing import Dict, List, Optional

from marshmallow_dataclass import dataclass
from sqlalchemy import Column, Integer, String, exists
from sqlalchemy.orm import Session, relationship

from app.extensions import Base
from app.models.machine_stock import MachineStock
from app.models.product import Product
from app.utils.result import Result


@dataclass
class VendingMachine(Base):
    machine_id: int
    location: str
    products: List[MachineStock]

    __tablename__ = "vending_machines"
    machine_id = Column(Integer, primary_key=True, autoincrement=True)
    location = Column(String(100))
    products = relationship("MachineStock", back_populates="vending_info", cascade="all,delete", lazy=True)

    @staticmethod
    def has_vending_machine_by_id(session: Session, machine_id: int) -> bool:
        return session.query(exists().where(VendingMachine.machine_id == machine_id)).scalar()

    @staticmethod
    def has_vending_machine_by_location(session: Session, location: str) -> bool:
        return session.query(exists().where(VendingMachine.location == location)).scalar()

    @staticmethod
    def get_vending_machine_by_id(session: Session, machine_id: str) -> Optional[VendingMachine]:
        try:
            machine_id = int(machine_id)
        except ValueError:
            return None
        return session.query(VendingMachine).filter(VendingMachine.machine_id == machine_id).first()

    @staticmethod
    def get_vending_machine_by_location(session: Session, location: str) -> Optional[VendingMachine]:
        return session.query(VendingMachine).filter(VendingMachine.location == location).first()

    @staticmethod
    def get_all_vending_machines(session: Session) -> Optional[List[VendingMachine]]:
        return session.query(VendingMachine).all()

    @staticmethod
    def create(session: Session, location: str) -> Result:
        if VendingMachine.has_vending_machine_by_location(session, location):
            return Result.fail("vending machine at that location already exists")
        new_machine = VendingMachine(location=location)
        return Result.success("vending machine created", new_machine)

    @staticmethod
    def delete_machine_by_id(session: Session, machine_id: str) -> Result:
        product_to_delete = VendingMachine.get_vending_machine_by_id(session, machine_id)
        if product_to_delete is None:
            return Result.fail("vending machine could not be found")
        session.delete(product_to_delete)
        session.commit()
        return Result.success("vending machine has successfully been deleted", product_to_delete)

    def add_product_by_id(self, session: Session, product_id: str, quantity: str) -> Result:
        try:
            product_id = int(product_id)
            quantity = int(quantity)
        except ValueError:
            return Result.fail("product_id or quantity are invalid")
        product_to_add = Product.has_product_by_id(session, product_id)
        if product_to_add is False:
            return Result.fail("product does not exist")
        if MachineStock.get_machine_stock(session, machine_id=self.machine_id, product_id=product_id) is not None:
            return Result.fail("this listing already exists, consider adding to the quantity instead")
        self.products.append(MachineStock(machine_id=self.machine_id, product_id=product_id, quantity=quantity))
        session.commit()
        return Result.success("product successfully added", self)

    def remove_product_by_id(self, session: Session, product_id: str) -> Result:
        try:
            product_id = int(product_id)
        except ValueError:
            return Result.fail("invalid product_id")

        if not Product.has_product_by_id(session, product_id):
            return Result.fail(f"product with product_id: {product_id} does not exist")

        return MachineStock.delete(session, self.machine_id, product_id)

    def increase_product_quantity_by_id(self, session: Session, product_id: str, quantity: str) -> Result:
        try:
            product_id = int(product_id)
            quantity = int(quantity)
        except ValueError:
            return Result.fail("product_id or quantity invalid")

        listing = MachineStock.get_machine_stock(session, machine_id=self.machine_id, product_id=product_id)
        if listing is None:
            return Result.fail("this product does not exist in the machine, consider adding it first")
        quantity_old = listing.quantity
        if listing.quantity + quantity < 0:
            return Result.fail("the final quantity cannot be negative")
        listing.quantity += quantity
        session.commit()
        return Result.success(
            f"product quantity successfully changed from" f" {quantity_old} to {listing.quantity}",
            listing,
        )

    def to_dict(self) -> Dict:
        return {
            "machine_id": self.machine_id,
            "location": self.location,
            "products": [i.to_dict for i in self.products],
        }
