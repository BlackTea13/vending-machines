from sqlalchemy import Column, ForeignKey, Integer, Text, String
from sqlalchemy.orm import relationship
from app import db

class Vending_machine(db.Model):
    
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