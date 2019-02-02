import json
import os
import sys
import time
import logging
#import jsonpath_rw
import io
import requests
import csv

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



#Everything below is based on : https://www.reddit.com/r/Sabermetrics/comments/99yvdc/statsapi_working_documentation/
#second comments

#NHL api seems better documented and very similar : https://github.com/dword4/nhlapi

list_of_dates = ["09/15/2017","09/16/2017","01/19/2017","09/17/2017","09/18/2017","09/19/2017"]
BASE_API_URL = "http://statsapi.mlb.com:80/api/v1/"



#this method makes one call per date returning all the IDs of the game played that day
#better implementation to make less call would be to make date ranges?
#this does not work : http://statsapi.mlb.com/api/v1/schedule?sportId=1&startdate=09/14/2017&enddate=09/17/2017
#this works : http://statsapi.mlb.com:80/api/v1/schedule?sportId=1&date=09/17/2017
def return_game_ids(date_list): # method to fetch gameIds for a given date
	dict_of_ids = {}
	for date in date_list:
		date_request = requests.get(url = "{}schedule?sportId=1&date={}".format(BASE_API_URL,date))
		if(date_request.json()["totalGames"] != 0):
			logger.info("Looking for games on {}".format(date))
			for games in date_request.json()["dates"][0]["games"]:
				dict_of_ids[games["gamePk"]] = date
		else:
			logger.warning("No games found on {}".format(date))
	return dict_of_ids


#method takes a game id returns stats for all players in the game
def return_player_stats_single_game(game_id):
	logger.info("Working on game with id : {}".format(game_id))
	game_request = requests.get(url = "{}game/{}/boxscore".format(BASE_API_URL,game_id))
	away_stats = complite_stats(game_request.json()["teams"]["away"])
	home_stats = complite_stats(game_request.json()["teams"]["home"])
	game_stats = {**away_stats,**home_stats}
	return game_stats


#compiling the stats ignoring cielding stats only taking pitching and batting
#only taking battin for batters and pitchingfor pitchers league where pitchers bat, those stats will be ignored
def complite_stats(stat_dict):
	ids_of_batters = stat_dict["batters"]
	ids_of_pitchers =  stat_dict["pitchers"]
	list_of_players = ids_of_batters + ids_of_pitchers
	result_dict = {}
	for ids in list_of_players:
		temp_dict = {}
		name = (stat_dict["players"]["ID{}".format(ids)]["person"]["fullName"]).replace(" ","_")
		temp_dict["position"] = stat_dict["players"]["ID{}".format(ids)]["position"]["abbreviation"]
		if(ids in ids_of_batters):
			if(stat_dict["players"]["ID{}".format(ids)]["stats"]["batting"] != {}):
				temp_dict["stats"] = stat_dict["players"]["ID{}".format(ids)]["stats"]["batting"]
		if(ids in ids_of_pitchers):
			if(stat_dict["players"]["ID{}".format(ids)]["stats"]["pitching"] != {}):
				temp_dict["stats"] = stat_dict["players"]["ID{}".format(ids)]["stats"]["pitching"]
		result_dict["{}_{}".format(name,ids)] = temp_dict
		logger.info("working on player : {}".format(name))
	return result_dict

def store_stats_in_tsv(date,game_stats):
	if(not os.path.exists("./data")):
		os.mkdir("./data")
	for players in game_stats.keys():
		if(not os.path.exists("./data/{}.csv".format(players))):
			header_row = ["date"] + ["position"] + list(game_stats[players]["stats"].keys())
			stats_row = [date] + [game_stats[players]["position"]] + list((game_stats[players]["stats"]).values())
			with open("./data/{}.csv".format(players), 'a') as csvFile:
				writer = csv.writer(csvFile)
				writer.writerow(header_row)
				writer.writerow(stats_row)
		else:
			stats_row = [date] + [game_stats[players]["position"]] + list((game_stats[players]["stats"]).values())
			with open("./data/{}.csv".format(players), 'a') as csvFile:
				writer = csv.writer(csvFile)
				writer.writerow(stats_row)
			




def main():
	game_ids = return_game_ids(list_of_dates)#call a function that returns a list with all dates for the range we want here to gather mass data
	for ids in game_ids.keys():
		store_stats_in_tsv(game_ids[ids],return_player_stats_single_game(ids))
main()








