from sqlalchemy import Column, Integer
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from database import DatabaseFactory

some_base = DatabaseFactory.Base

class DataStatline(some_base):
    __tablename__ = 'statline'
    id = Column(Integer, primary_key=True)
    hits = Column(Integer)
    gamelog = relationship("DataGamelog", uselist=False, backref="statline")

    def __init__(self, statline):
        self.hits = statline.categories["hits"]

#class User(Base): #statline
#    __tablename__ = 'user'

#    id = Column(Integer, primary_key=True)
#    name = Column(String)
#    mobile = relationship("Mobile", uselist=False, backref="owner")

#    def __init__(self, name):
#        self.name = name

