import csv
import os

from models import Player
from models import Statline
from models import Gamelog

class CsvReader():
    def __init__(self, *args, **kwargs):
        self.player = None
        self.gamelogs = []        
        return super().__init__()

    def _parse_filename(self, filepath):
        filename = os.path.splitext(os.path.basename(filepath))[0]
        tokens = filename.split('_')
        name = "{} {}".format(tokens[0], tokens[1])
        espn_id = tokens[2]
        self.player = Player(name, espn_id)
    
    def _parse_file(self, filepath):
        rows = []
        with open(filepath, newline='') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(map(lambda x: x, reader))
            relevant_rows = list(filter(None, rows))
            header = relevant_rows[0]
            categories_list = header[2:]
            gamelogs = relevant_rows[1:]
            for gamelog in gamelogs:
                date = gamelog[0]
                pos = gamelog[1]
                stats = gamelog[2:]
                assert len(stats) == len(categories_list)
                d = dict(zip(categories_list, stats))
                statline = Statline(d)
                self.gamelogs.append(Gamelog(date, pos, self.player, statline))

    def deserialize(self, filepath):
        self._parse_filename(filepath)
        self._parse_file(filepath)

