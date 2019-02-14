import csv
import os
from os import walk

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
root_dir = os.path.join(script_dir, '..')
data_path = os.path.join(root_dir, 'data')


def reader(filePath):
    with open(filePath, newline='') as csvfile:
        playerreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in playerreader:
            print(', '.join(row))

def parser():
    return []



def get_csv_files():
    f = []
    for (dirpath, dirnames, filenames) in walk(data_path):
        f.extend(filenames)        
    return f


for filename in get_csv_files():
    reader(os.path.join(data_path, filename))