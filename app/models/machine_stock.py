from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

from sqlalchemy import Column, ForeignKey, Integer, exists
from sqlalchemy.orm import Session, relationship

from app.extensions import Base
from app.models import vending_machine
from app.models.product import Product
from app.utils.result import Result


@dataclass
class MachineStock(Base):
    machine_id: int
    product_id: int
    quantity: int

    __tablename__ = "machine_stock"
    machine_id = Column(Integer, ForeignKey("vending_machines.machine_id"), primary_key=True)
    product_id = Column(Integer, ForeignKey("products.product_id"), primary_key=True)
    quantity = Column(Integer)

    product_info = relationship("Product", back_populates="machines", foreign_keys=[product_id], lazy=True)
    vending_info = relationship(
        "VendingMachine",
        back_populates="products",
        foreign_keys=[machine_id],
        lazy=True,
    )

    def to_dict(self) -> Dict:
        return {
            "product_id": self.product_id,
            "product_name": self.product_info.product_name,
            "product_price": self.product_info.price,
            "quantity": self.quantity,
        }

    @staticmethod
    def get_machine_stock(session: Session, machine_id: int, product_id: int) -> Optional[MachineStock]:
        return (
            session.query(MachineStock)
            .filter((MachineStock.product_id == product_id) & (MachineStock.machine_id == machine_id))
            .first()
        )

    @staticmethod
    def _get_listing_with_machine_and_product_id(
        session: Session, machine_id: int, product_id: int
    ) -> Optional[MachineStock]:  # pragma: no cover
        return session.query(
            exists().where(
                (vending_machine.VendingMachine.machine_id == machine_id) & (Product.product_id == product_id)
            )
        ).first()

    @staticmethod
    def delete(session: Session, machine_id: int, product_id: int) -> Result:  # pragma: no cover
        listing_to_delete = MachineStock._get_listing_with_machine_and_product_id(session, machine_id, product_id)
        if listing_to_delete is None:
            return Result.fail("this listing does not exist")
        session.delete(listing_to_delete)
        return Result.success("listing successfully deleted", listing_to_delete)
