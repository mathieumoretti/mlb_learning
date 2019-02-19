from sqlalchemy import Column, Integer
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

class Stats:
	def __init__(self, *args, **kwargs):
		self.stats = dict()
		return super().__init__(*args, **kwargs)

Base = declarative_base()
class DataStats(Base):
    __tablename__ = 'stats'
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('gamelog.id'))
    gamelog = relationship("DataGamelog", uselist=False, back_populates="stats")