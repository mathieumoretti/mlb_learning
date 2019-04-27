from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import DatabaseFactory

some_base = DatabaseFactory.Base

class DataPlayer(some_base):
    __tablename__ = 'player'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    gamelogs = relationship("DataGamelog", back_populates="player")

    def __init__(self, player):
        self.id = player.espn_id
        self.name = player.name

    def __eq__(self, other):
        return (self.id == other.id)

#class ProjectManager(Base): #Player
#    __tablename__ = 'project_manager'

#    id = Column(Integer, primary_key=True)
#    name = Column(String)
#    projects = relationship("Project", back_populates="project_manager")

#    def __init__(self, name):
#        self.name = name