from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

#import gamelog

class Player:
	def __init__(self, *args, **kwargs):
		self.name = ""
		self.game_logs = []
		return super().__init__(*args, **kwargs)

Base = declarative_base()
class DataPlayer(Base):
    __tablename__ = 'player'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    #game_logs = relationship("DataGamelog", back_populates="player")