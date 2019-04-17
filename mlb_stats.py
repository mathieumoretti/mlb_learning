import json
import os
import sys
import logging
#import jsonpath_rw
import io
import requests
import csv
import datetime
import time
import collections

file_name = os.path.basename(sys.argv[0])
log_name = file_name.replace("py", "log")
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s | %(name)s |  %(levelname)s: %(message)s')
logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)

file_handler = logging.FileHandler(filename=log_name,encoding = "utf-8")
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

start = time.time()


#Very simple predicitve model approach : 
#https://medium.freecodecamp.org/a-beginners-guide-to-training-and-deploying-machine-learning-models-using-python-48a313502e5a
#maybe feautures = average of stats last 3 game and label = runs + rbi


#Everything below is based on : https://www.reddit.com/r/Sabermetrics/comments/99yvdc/statsapi_working_documentation/
#second comments

#NHL api seems better documented and very similar : https://github.com/dword4/nhlapi

#list_of_dates = ["09/15/2017","09/16/2017","01/19/2017","09/17/2017","09/18/2017","09/19/2017"]
BASE_API_URL = "http://statsapi.mlb.com:80/api/v1/"
start_date = "01/01/2010"


#this method makes one call per date returning all the IDs of the game played that day
#better implementation to make less call would be to make date ranges?
#this does not work : http://statsapi.mlb.com/api/v1/schedule?sportId=1&startdate=09/14/2017&enddate=09/17/2017
#this works : http://statsapi.mlb.com:80/api/v1/schedule?sportId=1&date=09/17/2017
def return_game_ids(date): # method to fetch gameIds for a given date
	game_ids_list = []
	date_request = requests.get(url = "{}schedule?sportId=1&date={}".format(BASE_API_URL,date))
	if(date_request.json()["totalGames"] != 0):
		logger.debug("Looking for games on {}".format(date))
		for games in date_request.json()["dates"][0]["games"]:
			game_ids_list.append(games["gamePk"])
	else:
		logger.warning("No games found on {}".format(date))
		return []
	return game_ids_list.sort()

#method takes a game id returns stats for all players in the game
def return_player_stats_single_game(game_id,date):
	logger.debug("Working on game with id : {}".format(game_id))
	try:
		game_request = requests.get(url = "{}game/{}/boxscore".format(BASE_API_URL,game_id))
	
		date_request = requests.get(url = "{}game/{}/contextMetrics".format(BASE_API_URL,game_id))
		response_date = date_request.json()["game"]["gameDate"].split("T")[0]
		response_date = datetime.datetime.strptime(response_date, '%Y-%m-%d').strftime('%m/%d/%Y')
	except Exception as e:
		logger.error(e)
		return {}
	response_date_split = response_date.split("/")
	date_split = date.split("/")
	if(response_date_split[0] == date_split[0] and response_date_split[2] == date_split[2]):       #Problem Here wanna make sure the game id is from the same date...
		away_stats = compile_stats(game_request.json()["teams"]["away"])                           #Currently just making sure its same month and year or else get too many errors                                     
		home_stats = compile_stats(game_request.json()["teams"]["home"])
		game_stats = {**away_stats,**home_stats}
		return game_stats
	else:
		return {}


#compiling the stats ignoring cielding stats only taking pitching and batting
#only taking battin for batters and pitchingfor pitchers league where pitchers bat, those stats will be ignored
def compile_stats(stat_dict):
	try:
		ids_of_batters = stat_dict["batters"]
		ids_of_pitchers =  stat_dict["pitchers"]
		list_of_players = ids_of_batters + ids_of_pitchers
		result_dict = {}
		for ids in list_of_players:
			temp_dict = collections.OrderedDict()#make sure we get data in same order
			name = (stat_dict["players"]["ID{}".format(ids)]["person"]["fullName"]).replace(" ","_")
			temp_dict["position"] = stat_dict["players"]["ID{}".format(ids)]["position"]["abbreviation"]
			if(ids in ids_of_batters):
				if(stat_dict["players"]["ID{}".format(ids)]["stats"]["batting"] != {}):
					temp_dict["stats"] = stat_dict["players"]["ID{}".format(ids)]["stats"]["batting"]
			if(ids in ids_of_pitchers):
				if(stat_dict["players"]["ID{}".format(ids)]["stats"]["pitching"] != {}):
					temp_dict["stats"] = stat_dict["players"]["ID{}".format(ids)]["stats"]["pitching"]
			if("note" in temp_dict["stats"]):#remove note which is not always there and gives no info
				del temp_dict["stats"]["note"]
			result_dict["{}_{}".format(name,ids)] = temp_dict
			logger.debug("working on player : {}".format(name))
		return result_dict
	except Exception as e:
		logger.error(e)
		return {}

def store_stats_in_tsv(date,game_stats):

	if(game_stats != {}):
		if(not os.path.exists("./data")):
			os.mkdir("./data")
		for players in game_stats.keys():
			if(game_stats != {} and "stats" in game_stats[players] and "position" in game_stats[players]):
				sorted_stats = game_stats[players]["stats"]
				if("note" in sorted_stats):
					del sorted_stats["note"]
				if(not os.path.exists("./data/{}.csv".format(players))):

					header_row = ["date"] + ["position"] + list(sorted_stats.keys())
					stats_row = [date] + [game_stats[players]["position"]] + list(sorted_stats.values())
					with open("./data/{}.csv".format(players), 'a',newline='') as csvFile:
						writer = csv.writer(csvFile)
						writer.writerow(header_row)
						writer.writerow(stats_row)
				else:
					stats_row = [date] + [game_stats[players]["position"]] + list(sorted_stats.values())
					with open("./data/{}.csv".format(players), 'a',newline='') as csvFile:
						writer = csv.writer(csvFile)
						writer.writerow(stats_row)
	else:
		logger.error("Mix up in game IDs")
		return {}
		
			

def get_dates(date_one,date_two=datetime.datetime.today().strftime('%m/%d/%Y')):# gets all dates from date_one till now,second date can be overwritten
	date_list =[]
	d1 = datetime.datetime.strptime(date_one, '%m/%d/%Y')
	d2 = datetime.datetime.strptime(date_two, '%m/%d/%Y')
	diff = d2 - d1
	for i in range(diff.days + 1):
		date_list.append(str((d1 + datetime.timedelta(i)).strftime('%m/%d/%Y')))
	return date_list


def main():
	for dates in get_dates(start_date):
		game_ids_list = return_game_ids(dates)
		if(game_ids_list != []):
			for game_ids in game_ids_list:
				logger.info("Storing stats for date : {} ,game ID : {}".format(dates,game_ids))
				store_stats_in_tsv(dates,return_player_stats_single_game(game_ids,dates))
main()

end = time.time()
logger.info("Time of execution : {}".format(end - start))






def test_apis():
	request = requests.get(url = "{}schedule?sportId=1&date=07/07/2018".format(BASE_API_URL))
	assert(request.status_code == 200),"Schedule API not working"
	request = requests.get(url = "{}game/530732/boxscore".format(BASE_API_URL,game_id))
	assert(request.status_code == 200),"Game Stats API not working"