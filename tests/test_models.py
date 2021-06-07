import datetime

from mlb_learning.models import Categories
from mlb_learning.models import Gamelog
from mlb_learning.models import Player
from mlb_learning.models import Positions
from mlb_learning.models import Statline

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