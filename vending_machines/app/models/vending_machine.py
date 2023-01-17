from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.extensions import Base, Engine, Session
from flask import jsonify
from dataclasses import dataclass

@dataclass
class Vending_Machine(Base):
    machine_id : int
    location : str
    
    __tablename__ = 'vending_machines'
    machine_id = Column(Integer, primary_key = True, autoincrement=True)
    location = Column(String(1000))
    
    children = relationship("Machine_Stock")
    
    def __init__(self, location):
        self.location = location
        
    @staticmethod
    def find_machine_by_id(id: int):
        pass