from __future__ import annotations
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Session
from app.extensions import Base, Session
from dataclasses import dataclass
from typing import List, Dict, Optional
from app.models.machine_stock import MachineStock
from app.utils.result import Result
from app.models import product


@dataclass
class VendingMachine(Base):
    machine_id: int
    location: str
    machine_products: List[MachineStock]

    __tablename__ = 'vending_machines'
    machine_id = Column(Integer, primary_key=True,
                        autoincrement=True)
    location = Column(String(100))
    products = relationship("MachineStock", backref="vending_machine", cascade="all,delete", lazy=True)

    @property
    def machine_products(self) -> List[MachineStock]:
        machines = Session().query(MachineStock).filter_by(machine_id=self.machine_id).all()
        return [machine.to_dict() for machine in machines]

    @staticmethod
    def get_all_vending_machines(session: Session) -> Optional[List[VendingMachine]]:
        return session.query(VendingMachine).all()

    @staticmethod
    def create(session: Session, location: str) -> Result:
        new_machine = VendingMachine(location=location)
        return Result.success("vending machine created", new_machine)

    @staticmethod
    def get_product_id_in_object(vending_machine: VendingMachine,
                                 machine_stocks: List[MachineStock]) -> List[int]:
        machine_id = vending_machine.machine_id
        product_ids = [
            listing.product_id for listing in machine_stocks if machine_id == listing.machine_id]
        return product_ids

