import datetime
import os
from os import walk
import sys

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
root_dir = os.path.join(script_dir, '..')
data_path = os.path.join(root_dir, 'data')

sys.path.append(root_dir)


from models import Categories
from models import Gamelog
from models import Player
from models import Positions
from models import Statline

PLAYER_NAME = "James Bond"
PLAYER_ID = "007"
HITS = 1
DATE = datetime.date(1900,1,1)
POSITION_NAME = "pitcher"
CATEGORY_NAME = "hits"

def test_models():

    # constants
    category = Categories.HITS
    position = Positions.PITCHER

    assert category.name == CATEGORY_NAME
    assert position.name == POSITION_NAME

    # player
    player = Player(PLAYER_NAME, PLAYER_ID)

    assert player.name == PLAYER_NAME
    assert player.espn_id == PLAYER_ID

    # statline
    statline = Statline( dict(hits = HITS) )
    
    assert statline.categories[CATEGORY_NAME] == HITS

    # gamelog
    gamelog = Gamelog(DATE, position, player, statline)

    assert gamelog.date == DATE
    assert gamelog.position.name == POSITION_NAME
    assert gamelog.statline.categories[CATEGORY_NAME] == HITS
    assert gamelog.player.name == PLAYER_NAME
    assert gamelog.player.espn_id == PLAYER_ID

if __name__ == "__main__":
    test_models()