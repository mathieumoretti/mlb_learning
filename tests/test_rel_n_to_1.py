import datetime
import os
from os import walk
import sys

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
root_dir = os.path.join(script_dir, '..')
data_dir = os.path.join(root_dir, 'data')

sys.path.append(root_dir)

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Integer, Table, ForeignKey
from sqlalchemy.orm import relationship

from models import Gamelog
from models import Player
from models import Statline

from database import DataGamelog
from database import DataPlayer
from database import DataStatline

from database import DatabaseFactory

database_filename = 'db.sqlite_test'
database_dir = os.path.join(data_dir, 'database')
database_path = os.path.join(database_dir, database_filename)
db_uri =  os.path.join('sqlite:////', os.path.abspath(database_path))
db_uri_rel =  os.path.join('sqlite:///', database_filename)
if os.path.exists(database_filename):
    os.remove(database_filename)

engine = create_engine(db_uri_rel)

# use session_factory() to get a new Session
_SessionFactory = sessionmaker(bind=engine)

Base = DatabaseFactory.Base


def session_factory():
    Base.metadata.create_all(engine)
    return _SessionFactory()

def populate_database():
    session = session_factory()


    player1 = Player("James Bond", "007")
    data_player1 = DataPlayer(player1)

    gamelog1 = Gamelog(datetime.date(1900,1,1),"P")
    gamelog1.player = player1
    gamelog1.statline = Statline({})
    gamelog2 = Gamelog(datetime.date(1900,1,2),"P")
    gamelog2.player = player1
    gamelog2.statline = Statline({})

    data_statline1 = DataStatline(gamelog1.statline)
    data_statline2 = DataStatline(gamelog2.statline)
    data_gamelog1 = DataGamelog(gamelog1, data_player1, data_statline1)
    data_gamelog2 = DataGamelog(gamelog2, data_player1, data_statline2)

    session.add(data_gamelog1)
    session.add(data_gamelog2)

    session.commit()
    session.close()


def query_gamelogs():
    session = session_factory()
    gamelogs_query = session.query(DataGamelog)
    session.close()
    return gamelogs_query.all()


if __name__ == "__main__":
    gamelogs = query_gamelogs()
    if len(gamelogs) == 0:
        populate_database()

    gamelogs = query_gamelogs()
    for gamelog in gamelogs:
        print(f'"{gamelog.date}" is managed by {gamelog.player.name}')