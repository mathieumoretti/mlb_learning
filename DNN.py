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

#Very simple predicitve model approach : https://medium.freecodecamp.org/a-beginners-guide-to-training-and-deploying-machine-learning-models-using-python-48a313502e5a
# https://towardsdatascience.com/predicting-premier-league-odds-from-ea-player-bfdb52597392


class DNN:

	def __init__(self,num_of_games):#Class instantiates on the training and testing file 
		self.num_of_games = int(num_of_games)
		self.model_dir = 'model_{}'.format(self.num_of_games)

	def clean_data(self):
		logger.info("Creating clean data .....")
		counter = 0
		files_size = len(os.listdir("./data"))
		training_lenght = int(files_size*0.9)

		for filename in os.listdir("./data"):
			counter = counter + 1
			if(counter < training_lenght):
				file = "./data/{}".format(filename)
				read_data_one_file(self.num_of_games,file,"training_data_{}".format(self.num_of_games))
			else:
				file = "./data/{}".format(filename)
				read_data_one_file(self.num_of_games,file,"testing_data_{}".format(self.num_of_games))
		logger.info("Finished creating clean data .....")
		len_hitter_training = row_count("H_training_data_{}.csv".format(self.num_of_games))
		len_hitter_testing =  row_count("H_testing_data_{}.csv".format(self.num_of_games))
		logger.info("Created {} data rows for training".format(len_hitter_training))
		logger.info("Created {} data rows for testing".format(len_hitter_testing))


	def train(self):# training of neural network, needs to be tweaked for optimization is a long process
		train_features = {} 
		test_features = {}
		train_labels = []
		test_labels = []
		if(os.path.isdir(self.model_dir)):#Currently deleting model here on new training need to improve to keep training
			logger.info("Deleting folder : {}".format(self.model_dir))
			os.rmdir(self.model_dir)
		coldict = {}
		col_names = pd.read_csv("H_training_data_{}.csv".format(self.num_of_games)).columns
		for i in col_names:
			coldict[i] = int

		train_df = pd.read_csv("H_training_data_{}.csv".format(self.num_of_games),dtype=coldict)
		for idx,cols in enumerate(col_names):
			if(cols != "official_result" and cols != 'Unnamed: 0'):
				train_features[cols] = train_df.values[:, [idx]]
			elif(cols =="official_result"):
				train_labels = train_df.values[:, [idx]]
		test_df = pd.read_csv("H_testing_data_{}.csv".format(self.num_of_games),dtype=coldict)
		for idx,cols in enumerate(col_names):
			if(cols != "official_result" and cols != 'Unnamed: 0'):
				test_features[cols] = test_df.values[:, [idx]]
			elif(cols == "official_result"):
				test_labels = test_df.values[:, [idx]]

		feature_columns = []
		for idx,cols in enumerate(col_names):
			if(cols != "official_result" and cols != 'Unnamed: 0'):
				feature_columns.append(tf.feature_column.numeric_column(key=cols))

		#Magic happens here
		#model = tf.estimator.DNNClassifier( model_dir='model/',hidden_units=[23*8],feature_columns=feature_columns, n_classes=2,optimizer=tf.train.ProximalAdagradOptimizer(learning_rate=0.1,l1_regularization_strength=0.001))
		model = tf.estimator.DNNClassifier( model_dir=self.model_dir,hidden_units=[23*self.num_of_games],feature_columns=feature_columns, n_classes=2,
			optimizer=tf.train.ProximalAdagradOptimizer(learning_rate=0.1,l1_regularization_strength=0.001)
			)

		train_input_fn = tf.estimator.inputs.numpy_input_fn(x=train_features,y=train_labels,batch_size=32,num_epochs=100,shuffle=True)
		test_input_fn = tf.estimator.inputs.numpy_input_fn(x=test_features,y=test_labels,batch_size=32,num_epochs=100,shuffle=True)

		logger.info("Training model for : {} steps".format(len(train_labels)))
		model.train(input_fn=train_input_fn,steps =len(train_labels))
		evaluation_result = model.evaluate(input_fn=test_input_fn,steps = len(test_labels))

	def evaluate(self):# gives more detail about the accuracy of the Model
		test_labels = []
		test_features = {}

		coldict = {}
		col_names = pd.read_csv("H_testing_data_{}.csv".format(self.num_of_games), nrows=0).columns
		for i in col_names:
			coldict[i] = int

		test_df = pd.read_csv("H_testing_data_{}.csv".format(self.num_of_games),dtype=coldict)
		for idx,cols in enumerate(col_names):
			if(cols != "official_result" and cols != 'Unnamed: 0'):
				test_features[cols] = test_df.values[:, [idx]]
			elif(cols == "official_result"):
				test_labels = test_df.values[:, [idx]]
		list_of_results = [x[0] for x in test_labels.tolist()]#convert list of results to regular list(np.array to 1d list)
		feature_columns = []
		for idx,cols in enumerate(col_names):
			if(cols != "official_result" and cols != 'Unnamed: 0'):
				feature_columns.append(tf.feature_column.numeric_column(key=cols))
		print(test_features)
		model = tf.estimator.DNNClassifier( model_dir='model',hidden_units=[23*self.num_of_games],feature_columns=feature_columns, n_classes=2,
		optimizer=tf.train.ProximalAdagradOptimizer(learning_rate=0.1,l1_regularization_strength=0.001)
		)
		test_input_fn = tf.estimator.inputs.numpy_input_fn(x=test_features,shuffle = False)
		prediction = model.predict(test_input_fn)

		evaluate_scores(list(prediction),list_of_results)

	def predict(self,data_to_predict):#not tested placeholder for predict implementation


		model = tf.estimator.DNNClassifier( model_dir=self.model_dir,hidden_units=[23*self.num_of_games],feature_columns=feature_columns, n_classes=2,
		optimizer=tf.train.ProximalAdagradOptimizer(learning_rate=0.1,l1_regularization_strength=0.001)
		)
		test_input_fn = tf.estimator.inputs.numpy_input_fn(x=data_to_predict,shuffle = False)
		prediction = model.predict(test_input_fn)






def evaluate_scores(probability_list,hits):
	counter_1= 0
	counter = 0
	print("Evaluating score of : {} predictions".format(len(probability_list)))
	accuracy_counter_1=0
	accuracy_counter = 0
	for indx,value in enumerate(probability_list):
		prob_list = value["probabilities"].tolist()
		max_indx = prob_list.index(max(prob_list))
		if(max_indx != 0):
			counter_1 = counter_1 + 1
			#print(prob_list,hits[indx])
			if(max_indx == hits[indx]):
				accuracy_counter_1 = accuracy_counter_1 + 1
		else:
			counter = counter+1
			if(max_indx == hits[indx]):
				accuracy_counter = accuracy_counter + 1
	logger.info("Accuracy when not predicting 0 : " + str(accuracy_counter_1/counter_1))
	logger.info("Accuracy when predicting 0 : " + str(accuracy_counter/counter))


def return_data_P_one_row(dct):
	data_list = []
	for i in dct:
		if(i != "date" and i != "position" and i != "note"and i != "gamesPlayed"and i):
			data_list.append(dct[i])
	return data_list

def return_data_P_one_header(dct,lenght):
	header_list = []
	temp_list =[]
	for counter in range(lenght):
		temp_list = []
		for i in dct:
			if(i != "date" and i != "position" and i != "note"and i != "gamesPlayed"and i):
				temp_list.append(i+str(counter))
		header_list = header_list + temp_list
	return header_list

def return_data_H_one_row(dct):
	data_list = []
	for i in dct:
		if(i != "date" and i != "position" and i != "note"and i != "gamesPlayed"and i):
			data_list.append(dct[i])
	return data_list


def return_data_H_one_header(dct,lenght):
	header_list = []
	temp_list =[]
	for counter in range(lenght):
		temp_list = []
		for i in dct:
			if(i != "date" and i != "position" and i != "note"and i != "gamesPlayed"and i):
				temp_list.append(i+str(counter))
		header_list = header_list + temp_list
	return header_list




def read_data_one_file(lenght,filename,output_file):
	counter = 0
	final_list = []
	holder_list = []
	with open(filename) as f:
		myreader = csv.DictReader(f)
		row_count = len(list(myreader))
		if(row_count < lenght + 2):
			return
	with open(filename) as f:
		reader = csv.DictReader(f)
		for dct in map(dict, reader):
			if(dct["position"] == "P"):
				position = "P"
				data_list = return_data_P_one_row(dct)
				try:
					for i in data_list:
						i = int(float(i))
				except Exception as e:
					logger.error(e)
					return
				header_list = return_data_P_one_header(dct,lenght)
				holder_list.append(data_list)
				if(len(holder_list) == lenght  + 1):
					if("inningsPitched" in dct):
						if(dct["runs"] and dct["rbi"] and dct["inningsPitched"]):
							try:
								temp_list = []
								for size in range(lenght):
									temp_list = temp_list + holder_list[size]
								final_list.append([temp_list,float(dct["runs"] + dct["rbi"])/float(dct["inningsPitched"])])
								del holder_list[0]
							except Exception as e:
								logger.error(e)
								return
				else:
					return
				return
			else:
				position = "H"
				data_list = return_data_H_one_row(dct)
				try:
					for i in data_list:
						i = int(float(i))
				except Exception as e:
					logger.error(e)
					return
				header_list = return_data_H_one_header(dct,lenght)
				holder_list.append(data_list)
				if(len(holder_list) == lenght  + 1):
					if(dct["rbi"] and dct["runs"]):
						feature_value = int(dct["rbi"]) + int(dct["runs"])
						if(feature_value >= 1):# more than one hits = 1 hit
							feature_value = 1
						temp_list = []
						for size in range(lenght):
							temp_list = temp_list + holder_list[size]
						final_list.append([temp_list,feature_value])
						del holder_list[0]
					else:
						logger.error("rbi or runs were not in data")
						return
	
	logger.info("Adding data for filename : {}  ".format(filename))
	if(position == "H"):
		if(not os.path.isfile("{}_{}.csv".format(position,output_file))):
			logger.info("Adding header row for hitters")
			with open("{}_{}.csv".format(position,output_file),'w+',newline='') as csvFile:
				writer = csv.writer(csvFile)
				writer.writerow(header_list + ["official_result"])
		else:
			with open("{}_{}.csv".format(position,output_file), 'a',newline='') as csvFile:
				writer = csv.writer(csvFile)
				for i in range(len(final_list)):
					writer.writerow(final_list[i][0] + [final_list[i][1]]) 
	
	if(position == "P"):
		if(not os.path.isfile("{}_{}.csv".format(position,output_file))):
			logger.info("Adding header row for Pitchers")
			with open("{}_{}".format(position,output_file),'w+',newline='') as csvFile:
				writer = csv.writer(csvFile)
				writer.writerow(header_list + ["official_result"])
		else:
			with open("{}_{}.csv".format(position,output_file), 'a',newline='') as csvFile:
				writer = csv.writer(csvFile)
				for i in range(len(final_list)):
					writer.writerow(final_list[i][0] + [final_list[i][1]]) 


	return

def row_count(input):
    with open(input) as f:
        for i, l in enumerate(f):
            pass
    return i
