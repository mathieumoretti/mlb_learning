
# content of test_sample.py
def test_database():
    someVar = 2
    assert 2 == someVar

import datetime
import os
from os import walk
import sys

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
root_dir = os.path.join(script_dir, '..')
data_path = os.path.join(root_dir, 'data')

sys.path.append(root_dir)

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Integer, Table, ForeignKey
from sqlalchemy.orm import relationship



db_uri = 'sqlite:///db.sqlite_test'
engine = create_engine(db_uri)
# use session_factory() to get a new Session
_SessionFactory = sessionmaker(bind=engine)


from models import Categories
from models import Player
from models import Gamelog
from models import Statline
from database import DataPlayer
from database import DataGamelog
from database import DataStatline
from database import DatabaseFactory


some_base = DatabaseFactory.Base

def session_factory():
    some_base.metadata.create_all(engine)
    return _SessionFactory()


class Mobile(some_base): #gamelog
    __tablename__ = 'mobile'

    id = Column(Integer, primary_key=True)
    model = Column(String)
    number = Column(String)
    owner_id = Column(Integer, ForeignKey('user.id'))

    def __init__(self, model, number, owner):
        self.model = model
        self.number = number
        self.owner = owner

class User(some_base): #statline
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    mobile = relationship("Mobile", uselist=False, backref="owner")

    def __init__(self, name):
        self.name = name


def populate_database():
    session = session_factory()

    bruno = User("Bruno Krebs")
    john = User("John Doe")

    brunos_mobile = Mobile("android", "99991111", bruno)
    johns_mobile = Mobile("iphone", "55554444", john)

    session.add(brunos_mobile)
    session.add(johns_mobile)

    session.commit()
    session.close()


def query_users():
    session = session_factory()
    users_query = session.query(User)
    session.close()
    return users_query.all()


def query_mobiles():
    session = session_factory()
    mobiles_query = session.query(Mobile)
    session.close()
    return mobiles_query.all()


def test_database():

    #category = Categories.HITS

    ## A default model
    #stat1 =  Statline()
    #statistics = []
    #statistics.append(stat1)

    #data_statline = DataStatline(stat1)

    #aDate = datetime.date(1900,1,1)

    #gamelog1 = Gamelog()
    #gamelog1.date = aDate
    #gamelog1.position = "P"
    #gamelog1.stats = stat1

    #data_gamelog = DataGamelog(gamelog1.date, gamelog1.position, data_statline)

    #gamelogs = []
    #gamelogs.append(gamelog1)

    #player1 = Player()
    #player1.name = "James Bond"
    #player1.espn_id = "007"
    #player1.game_logs = gamelogs

    #data_player1 = DataPlayer(player1.name,  player1.espn_id)

    #player2 = Player()
    #player2.name = "Alec Trevalian"
    #player2.espn_id = "006"
    #player2.game_logs = gamelogs

    #data_player2 = DataPlayer(player2.name,  player2.espn_id)



    users = query_users()
    #if len(users) == 0:
    #    populate_database()

    #users = query_users()
    #for user in users:
    #    print(f'{user.name} has an {user.mobile.model} with number {user.mobile.number}')

    #someVar = 2
    #assert 2 == someVar

if __name__ == "__main__":
    test_database()



        #d = dict(zip(categories_list, values))
        #statline = {stat_header[x]: stat_header[x] for x in range(0, len(gamestats) - 1)}
        #stat = Statline()
        #stat.fill(statline)

        #gamelog = Gamelog(log[0], log[1], player, )
        #gamelog.date = log[0]
        #gamelog.position = log[1]
        #gamestats = log[2:]
