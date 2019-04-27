from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from database import DatabaseFactory

some_base = DatabaseFactory.Base

class DataGamelog(some_base):
    __tablename__ = 'gamelog'
    id = Column(Integer, primary_key=True)
    date = Column(String)
    position = Column(String)
    statline_id = Column(Integer, ForeignKey('statline.id'))
    player_id = Column(Integer, ForeignKey('player.id'))
    player = relationship("DataPlayer", back_populates="gamelogs")
   
    def __init__(self, gamelog, data_player, data_statline):
        self.date = gamelog.date
        self.position = gamelog.position
        self.player = data_player
        self.statline = data_statline


#class Mobile(Base): #gamelog
#    __tablename__ = 'mobile'

#    id = Column(Integer, primary_key=True)
#    model = Column(String)
#    number = Column(String)
#    owner_id = Column(Integer, ForeignKey('user.id'))

#    def __init__(self, model, number, owner):
#        self.model = model
#        self.number = number
#        self.owner = owner

#class Project(Base): #Gamelog
#    __tablename__ = 'project'

#    id = Column(Integer, primary_key=True)
#    title = Column(String)
#    description = Column(String)
#    #player_id
#    project_manager_id = Column(Integer, ForeignKey('project_manager.id'))
#    project_manager = relationship("ProjectManager", back_populates="projects")

#    def __init__(self, title, description, project_manager):
#        self.title = title
#        self.description = description
#        self.project_manager = project_manager