import datetime
import os
from os import SEEK_CUR, walk
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

from mlb_learning.models import Categories
from mlb_learning.models import Player
from mlb_learning.models import Gamelog
from mlb_learning.models import Statline
from database import DataPlayer
from database import DataGamelog
from database import DataStatline
from database import DatabaseFactory

some_base = DatabaseFactory.Base

def session_factory():
    some_base.metadata.create_all(engine)
    return _SessionFactory()


def test_database():
    # Clean-all
    session = session_factory()
    session.query(DataPlayer).delete()
    session.query(DataStatline).delete()
    
    # Create
    jamesBond = Player("James Bond", 7)
    data_player1 = DataPlayer(jamesBond.name,  jamesBond.espn_id)

    alecTrevalian = Player("Alec Trevalian", 6)
    data_player2 = DataPlayer(alecTrevalian.name,  alecTrevalian.espn_id)

    austinPowers = Player("Austin Powers", 69)
    data_player3 = DataPlayer(austinPowers.name,  austinPowers.espn_id)

    statline = Statline(dict(hits = 1))
    data_statline = DataStatline(statline)
    
    session.add(data_player1)
    session.add(data_player2)
    session.add(data_statline)

    session.commit()

    # Read    
    players = session.query(DataPlayer).all()
    assert players[0].name == jamesBond.name
    assert players[0].espn_id == jamesBond.espn_id
    assert players[1].name == alecTrevalian.name
    assert players[1].espn_id == alecTrevalian.espn_id

    statlines = session.query(DataStatline).all()
    assert statlines[0].hits == statline.categories[Categories.HITS.name]
    
    # Update
    session.query(DataPlayer).filter(DataPlayer.espn_id == jamesBond.espn_id).update({"name": data_player3.name, "espn_id" : data_player3.espn_id})
    
    session.query(DataStatline).filter(DataStatline.hits == 1).update({"hits": 2})
    session.commit()
    players = session.query(DataPlayer).all()
    assert players[0].name == austinPowers.name
    assert players[0].espn_id == austinPowers.espn_id

    statlines = session.query(DataStatline).all()
    assert statlines[0].hits == 2

    # Delete
    session.delete(players[0])    
    players = session.query(DataPlayer).all()
    assert players[0].name == alecTrevalian.name
    assert players[0].espn_id == alecTrevalian.espn_id

    session.delete(players[0])   
    assert session.query(DataPlayer).filter_by(name=alecTrevalian.name).count() == 0
    
    session.delete(statlines[0])   
    assert session.query(DataStatline).filter_by(hits=2).count() == 0
    session.close()

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



    ##users = query_users()



