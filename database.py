from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer, String, Date
from sqlalchemy import inspect

# TODO:move to config file // environment  
db_uri = 'sqlite:///db.sqlite'

def drop_all(meta):
    meta.drop_all()

def create_all(meta):
    tempTables = [] 
    t1 = Table('Player', meta,
               Column('id', Integer, primary_key=True),
               Column('name',String))
    tempTables.append(t1)
    t2 = Table('Gamelog', meta,
               Column('id', Integer, primary_key=True),
               Column('date',Date))
    tempTables.append(t2)
    t3 = Table('Stats', meta,
               Column('id', Integer, primary_key=True),
               Column('atbats',Date))
    tempTables.append(t3)
    meta.create_all()
    return tempTables

def main():
    engine = create_engine(db_uri)
    meta = MetaData(engine)
    
    drop_all(meta)
    tables = create_all(meta)

    inspector = inspect(engine)

    # Get table information
    print('table_info')
    table_names = inspector.get_table_names()
    print("Number of tables:{}".format(len(table_names)))
    print(table_names)

if __name__ == "__main__":
    main()



#t4 rel between player and gamelog 1 to n or n to m
#t5 rel between gamelog and stats  1 to 1







