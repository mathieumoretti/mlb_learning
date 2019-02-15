from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker

from player import DataPlayer
from gamelog import DataGamelog

import json

# TODO:move to config file // environment  
db_uri = 'sqlite:///db.sqlite_test_create'
creation_mode = 'models'

Session = sessionmaker()

def create_all(session):

    player = DataPlayer(name='Ed')
    session.add(player)
   

def inspect_all(engine):
    inspector = inspect(engine)

    # Get table information
    print('table_info')
    table_names = inspector.get_table_names()
    print("Number of tables:{}".format(len(table_names)))
    print(table_names)

def main():
    engine = create_engine(db_uri)
    meta = MetaData(engine)
    Session.configure(bind=engine)
    session = Session()
    create_all(session)
    session.close()

if __name__ == "__main__":
    main()

