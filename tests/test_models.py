import datetime
import os
from os import walk
import sys

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
root_dir = os.path.join(script_dir, '..')
data_path = os.path.join(root_dir, 'data')

sys.path.append(root_dir)

from models import Player
from models import Gamelog
from models import Statline
from models import Categories

PLAYER_NAME = "James Bond"
PLAYER_ID = "007"
HITS = 1
DATE = datetime.date(1900,1,1)
PLAYER_POS = "P"
CATEGORY_NAME = "hits"


def test_models():
    category = Categories.HITS
    categories = Categories.get_categories()
    player = Player(PLAYER_NAME, PLAYER_ID)
    statline = Statline( dict(hits = HITS) )
    gamelog = Gamelog(DATE, PLAYER_POS, player, statline)

    assert category.name == CATEGORY_NAME
    assert gamelog.date == DATE
    assert gamelog.position == PLAYER_POS
    assert gamelog.statline.categories[CATEGORY_NAME] == HITS
    assert gamelog.player.name == PLAYER_NAME
    assert gamelog.player.espn_id == PLAYER_ID

if __name__ == "__main__":
    test_models()