from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.extensions import Base, Engine, Session

Base.metadata.create_all(Engine)

class Machine_Stock(Base):
    __tablename__ = 'machine_stock'
    machine_stock_id = Column(Integer, primary_key = True, autoincrement=True)
    machine_id = Column(Integer, ForeignKey('machine.id'))
    product_id = Column(Integer, ForeignKey('product.id'))
    
    
    