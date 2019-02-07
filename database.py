from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer, String, Date
from sqlalchemy import inspect

db_uri = 'sqlite:///db.sqlite'
engine = create_engine(db_uri)

meta = MetaData(engine)
t1 = Table('Player', meta,
           Column('id', Integer, primary_key=True),
           Column('name',String))
t2 = Table('Gamelog', meta,
           Column('id', Integer, primary_key=True),
           Column('date',Date))
t3 = Table('Stats', meta,
           Column('id', Integer, primary_key=True),
           Column('date',Date))
t1.create()

inspector = inspect(engine)

# Get table information
print(inspector.get_table_names())


