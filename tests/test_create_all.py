import datetime
import os
from os import walk
import sys

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
root_dir = os.path.join(script_dir, '..')
data_dir = os.path.join(root_dir, 'data')

sys.path.append(root_dir)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Categories
from models import Player
from models import Gamelog
from models import Statline
from database import DataPlayer
from database import DataGamelog
from database import DataStatline
from database import DatabaseFactory

from utils import CsvReader
from utils import CsvCollector

#globals
NO_OF_FILES = 5
gamelogs = [] 

database_filename = 'db.sqlite_main'
database_dir = os.path.join(data_dir, 'database')
database_path = os.path.join(database_dir, database_filename)
db_uri =  os.path.join('sqlite:////', os.path.abspath(database_path))
db_uri_rel =  os.path.join('sqlite:///', database_filename)
if os.path.exists(database_filename):
    os.remove(database_filename)

engine = create_engine(db_uri_rel)
# use session_factory() to get a new Session
_SessionFactory = sessionmaker(bind=engine)

some_base = DatabaseFactory.Base

def session_factory():
    some_base.metadata.create_all(engine)
    return _SessionFactory()

def collect_csv_files():
    collector = CsvCollector()
    collector.collect(data_dir)
    return collector.files

def parse_csv_files(files):
    for filepath in files[0:len(files)]:
        reader = CsvReader()
        reader.deserialize(filepath)        
        gamelogs.extend(reader.gamelogs) # could convert to a set

def populate_database(gl):
    session = session_factory()

    data_players = {}
    for g in gl:
        data_statline = DataStatline(g.statline)
        
        if g.player.espn_id in data_players:
            data_player = data_players[g.player.espn_id]
        else:
            data_player = DataPlayer(g.player)
            data_players[g.player.espn_id] = data_player

        session.add(DataGamelog(g, data_player, data_statline))

    session.commit()
    session.close()


def test_database():
    files = collect_csv_files()
    #assert len(files) >= NO_OF_FILES 
    parse_csv_files(files)
    #assert len(gamelogs) >= 0
    populate_database(gamelogs)

   # users = query_users()
    #if len(users) == 0:
    #    populate_database()

    #users = query_users()
    #for user in users:
    #    print(f'{user.name} has an {user.mobile.model} with number {user.mobile.number}')

    #someVar = 2
    #assert 2 == someVar

if __name__ == "__main__":
    test_database()