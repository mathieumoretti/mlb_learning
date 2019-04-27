from sqlalchemy import Column, Integer, Table
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from models import Categories
from database import DatabaseFactory

some_base = DatabaseFactory.Base

primary_key = [Column('id', Integer, primary_key=True)]
column_list = primary_key + list(map(lambda x: Column(x.name, Integer), Categories.get_categories()))
columns = tuple(column_list)
class DataStatline(some_base):
    __table__ = Table('statline', some_base.metadata, *columns)

    gamelog = relationship("DataGamelog", uselist=False, backref="statline")

    def __init__(self, statline):
        for key,value in statline.categories.items():
            setattr(self, key, value)

#class User(Base): #statline
#    __tablename__ = 'user'

#    id = Column(Integer, primary_key=True)
#    name = Column(String)
#    mobile = relationship("Mobile", uselist=False, backref="owner")

#    def __init__(self, name):
#        self.name = name

