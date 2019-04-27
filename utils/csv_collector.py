import os
from os import walk

class CsvCollector:
    def __init__(self, *args, **kwargs):
        self.files = []
        return super().__init__()

    def collect(self, csv_directory_path):
        self.files = []
        for (dirpath, dirnames, filenames) in walk(csv_directory_path):
            self.files.extend([os.path.join(dirpath,x) for x in filenames])