import csv
import os
from os import walk

from mlb_learning.player import Player
from models.player import Player

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
root_dir = os.path.join(script_dir, '..')
data_path = os.path.join(root_dir, 'data')

def read_csv(filePath):
    rows = []
    with open(filePath, newline='') as csvfile:
        playerreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in playerreader:
            rows.append(row)
            #print(', '.join(row))
    

    raw_logs = list(filter(None, rows))
    print(raw_logs)
    return raw_logs

def collect_csv_files():
    f = []
    for (dirpath, dirnames, filenames) in walk(data_path):
        f.extend([os.path.join(dirpath,x) for x in filenames])        
    return f


for filepath in collect_csv_files():
    # maybe use regex
    filename = os.path.splitext(os.path.basename(filepath))[0]
    tokens = filename.split('_')
    first_name = tokens[0]
    last_name = tokens[1]
    espn_id = tokens[2]

    player = models.Player()
    player.first_name = first_name
    player.last_name = last_name
    player.espn_id = id

    logs = read_csv(filepath)
    gamelogs = logs[1:]