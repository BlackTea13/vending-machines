from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.extensions import Base, Engine, Session

Base.metadata.create_all(Engine)

class Vending_Machine(Base):
    __tablename__ = 'vending_machines'
    machine_id = Column(Integer, primary_key = True, autoincrement=True)
    location = Column(String(1000))
    
    machine_stock = relationship("machine_stock", backref="machine")
    
    def __init__(self, machine_id, location):
        self.machine_id = machine_id
        self.location = location
        
    @staticmethod
    def find_machine_by_id(id: int):
        pass