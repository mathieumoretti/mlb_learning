import os
from os import walk
import sys

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
root_dir = os.path.join(script_dir, '..')
data_path = os.path.join(root_dir, 'data')

sys.path.append(root_dir)

from utils import CsvReader

NO_OF_FILES = 5
players = []
gamelogs = [] # list of gamelogs


def collect_csv_files():
    f = []
    for (dirpath, dirnames, filenames) in walk(data_path):
        f.extend([os.path.join(dirpath,x) for x in filenames])        
    return f

def test_readcsv():
    files = collect_csv_files()
    assert len(files) >= NO_OF_FILES
    for filepath in files[0:NO_OF_FILES]:

        reader = CsvReader()
        reader.deserialize(filepath)
        players.append(reader.player)
        for gamelog in reader.gamelogs:
            gamelogs.append(gamelog)

    assert len(players) == NO_OF_FILES
    assert len(gamelogs) >= NO_OF_FILES

if __name__ == "__main__":
    test_readcsv()


