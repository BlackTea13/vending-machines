from sqlalchemy import Column, Integer, String, Float
from app.extensions import Base, Engine, Session

Base.metadata.create_all(Engine)

class Machine_Stock(Base):
    __tablename__ = 'machine_stock'
    product_id = Column(Integer, primary_key = True, autoincrement=True)
    product_name = Column(String(1000))
    price = Column(Float)