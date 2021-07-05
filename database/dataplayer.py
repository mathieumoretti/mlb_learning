from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import DatabaseFactory

some_base = DatabaseFactory.Base

class DataPlayer(some_base):
    __tablename__ = 'player'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    espn_id = Column(Integer, nullable=False, default=-1)    

    def __init__(self, name, espn_id):
        self.name = name
        self.espn_id = espn_id
