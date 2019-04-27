import os
import sys

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
root_dir = os.path.join(script_dir, '..')
data_path = os.path.join(root_dir, 'data')

sys.path.append(root_dir)

from utils import CsvReader
from utils import CsvCollector

#globals
NO_OF_FILES = 5
players = []
gamelogs = [] 
statlines = []

def test_readcsv():
    collector = CsvCollector()
    collector.collect(data_path)
    files = collector.files
    assert len(files) >= NO_OF_FILES
    for filepath in files[0:NO_OF_FILES]:

        reader = CsvReader()
        reader.deserialize(filepath)
        players.append(reader.player)
        for gamelog in reader.gamelogs:
            gamelogs.append(gamelog)

        for statline in reader.statlines:
            statlines.append(statline)

    assert len(players) == NO_OF_FILES
    assert len(gamelogs) >= NO_OF_FILES
    assert len(statlines) == len(gamelogs)

if __name__ == "__main__":
    test_readcsv()


