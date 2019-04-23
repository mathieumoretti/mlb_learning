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

from models import Statline
from models import Gamelog

from database import DataGamelog
from database import DataStatline

from database import DatabaseFactory

database_filename = 'db.sqlite'
database_dir = os.path.join(data_dir, 'database')
database_path = os.path.join(database_dir, database_filename)
db_uri =  os.path.join('sqlite:////', os.path.abspath(database_path))
db_uri_rel =  os.path.join('sqlite:///', database_filename)
if os.path.exists(database_filename):
    os.remove(database_filename)

engine = create_engine(db_uri_rel)
# use session_factory() to get a new Session
_SessionFactory = sessionmaker(bind=engine)

def session_factory():
    DatabaseFactory.Base.metadata.create_all(engine)
    return _SessionFactory()

def populate_database():
    session = session_factory()

    stat1 =  Statline()
    data_statline1 = DataStatline(stat1)

    stat2 =  Statline()
    stat2.categories["hits"] = 2
    data_statline2 = DataStatline(stat2)

    gamelog1 = Gamelog()
    gamelog1.date = datetime.date(1900,1,1)
    gamelog1.position = "P"
    gamelog1.stats = stat1

    data_gamelog1 = DataGamelog(gamelog1.date, gamelog1.position, data_statline1)
 
    gamelog2 = Gamelog()
    gamelog2.date = datetime.date(1900,1,2)
    gamelog2.position = "P"
    gamelog2.stats = stat2

    data_gamelog2 = DataGamelog(gamelog2.date, gamelog2.position, data_statline2)

    session.add(data_gamelog1)
    session.add(data_gamelog2)

    session.commit()
    session.close()

def query_statlines():
    session = session_factory()
    statline_query = session.query(DataStatline)
    session.close()
    return statline_query.all()


def query_gamelogs():
    session = session_factory()
    gamelogs_query = session.query(DataGamelog)
    session.close()
    return gamelogs_query.all()

if __name__ == "__main__":
    statlines = query_statlines()
    if len(statlines) == 0:
        populate_database()

    statlines = query_statlines()
    for statline in statlines:
        print(f'{statline.hits} on {statline.gamelog.date} with number {statline.gamelog.position}')