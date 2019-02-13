from sqlalchemy import Column, Integer
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

#from player import DataPlayer

class GameLog:
	def __init__(self, *args, **kwargs):
		self.date = ""
		self.stats = ""
		return super().__init__(*args, **kwargs)

Base = declarative_base()
class DataGamelog(Base):
    __tablename__ = 'gamelog'
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('player.id'))
    player = relationship("DataPlayer", foreign_keys=player_id, back_populates="gamelog")
    stats = relationship("DataStats", uselist=False, back_populates="gamelog")