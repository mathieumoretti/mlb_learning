import os
import sys
import logging
#import jsonpath_rw
import csv
import time
import pandas as pd
import numpy as np
from sklearn import linear_model
import glob
import pickle
# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras
from DNN import DNN


file_name = os.path.basename(sys.argv[0])
log_name = file_name.replace("py", "log")
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s | %(name)s |  %(levelname)s: %(message)s')
logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)

file_handler = logging.FileHandler(filename=log_name,encoding = "utf-8")
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)
tf.logging.set_verbosity(tf.logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument("-n","--number_of_games_previous",help="Number of games to base the prediction of the next game on")

args = parser.parse_args()

start = time.time()





if __name__ == "__main__":
	MLB_NN = DNN(args.number_of_games_previous)
	MLB_NN.clean_data()
	MLB_NN.train()
	MLB_NN.evaluate()


end = time.time()
logger.info("Time of execution : {}".format(end - start))






