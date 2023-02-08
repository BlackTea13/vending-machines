from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from marshmallow_dataclass import dataclass
from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer

from app.extensions import Base, Session
from app.models import machine_stock, vending_machine
from app.utils.result import Result


@dataclass
class StockTimeline(Base):
    time: DateTime
    machine_id: int
    product_id: int
    product_quantity: int
    stock_state: JSON

    __tablename__ = "stock_timeline"
    time = Column(DateTime, primary_key=True, default=datetime.now())
    machine_id = Column(Integer, ForeignKey("vending_machines.machine_id"), primary_key=True)
    product_id = Column(Integer, ForeignKey("products.product_id"))
    product_quantity = Column(Integer)
    stock_state = Column(JSON)

    @staticmethod
    def save_state(session: Session, machine_id: int, product_id: int) -> Result:
        if machine_id is None:
            return Result.fail("machine_id cannot be None-type object")
        if product_id is None:
            return Result.fail("product_id cannot be None-type object")

        try:
            stock = (
                session.query(machine_stock.MachineStock)
                .filter(
                    (machine_stock.MachineStock.product_id == product_id)
                    & (machine_stock.MachineStock.machine_id == machine_id)  # noqa: W503
                )
                .first()
            )

            date = datetime.now()

            if stock.quantity < 0:
                return Result.fail("quantity cannot be lower than 1")

            products = vending_machine.VendingMachine.get_vending_machine_by_id(session, str(machine_id))
            state = [i.to_dict() for i in products.products]
            print(state)

            print("HJiudhsafiuahoighareuubioahgoiuaehgiourhIOUGHARIUORGH=-====================")
            column = StockTimeline(
                time=date,
                machine_id=machine_id,
                product_id=product_id,
                product_quantity=stock.quantity,
                stock_state=state,
            )
            session.add(column)
            session.commit()
            return Result.success("Snapped", None)
        except Exception as e:
            print(f"Something went wrong  {e}")
            return Result.fail(f"Something went wrong : {e}")

    @staticmethod
    def product_time_stamp_in_records(product_id: int) -> Optional[List["StockTimeline"]]:
        stock_record = Session().query(StockTimeline).filter_by(product_id=product_id).all()
        return stock_record

    @staticmethod
    def machine_time_stamp_in_records(machine_id: int) -> Optional[List["StockTimeline"]]:
        stock_record = Session().query(StockTimeline).filter_by(machine_id=machine_id).all()
        return stock_record
