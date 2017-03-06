import urllib2
import json

def get_event_list():
	url = "http://www.thebluealliance.com/api/v2/events/2017" + '?X-TBA-App-Id=frc8%3Asteamworks-takeoff-analysis%3Atest'
	request = urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'})
	data = urllib2.urlopen(request).read().decode('utf-8')
	jsonvar = json.loads(data)

	return_val = []
	for i in jsonvar:
		return_val.append(Event(i))
	return return_val

def get_match(matchkey):
	url = "http://www.thebluealliance.com/api/v2/match/" + matchkey + '?X-TBA-App-Id=frc8%3Afantasy-league%3Adev'
	request = urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'})
	data = urllib2.urlopen(request).read().decode('utf-8')
	jsonvar = json.loads(data)

	return Match(jsonvar)

def get_matches(eventKey):
	url = "http://www.thebluealliance.com/api/v2/event/" + eventKey + "/matches" + '?X-TBA-App-Id=frc8%3Afantasy-league%3Adev'
	request = urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'})
	data = urllib2.urlopen(request).read().decode('utf-8')
	jsonvar = json.loads(data)

	return_val = []
	for i in jsonvar:
		return_val.append(Match(i))
	return return_val

class Event(object):
	def __init__(self, event_dict):
		self.real_data = event_dict
		self.key = event_dict["key"]
		self.name = event_dict["name"]
		self.event_type_string = event_dict["event_type_string"]
		self.week = event_dict["week"]

	def get_key(self):
		return self.key

	def get_name(self):
		return self.name

	def get_event_type(self):
		return self.event_type_string

	def get_week(self):
		if self.key == "2017cmptx":
			return 8
		if self.key == "2017cmpmo":
			return 9
		if not isinstance(self.week, int):
			return -1
		return int(self.week) + 1

class Match(object):
	def __init__(self, match_dict):
		self.real_data = match_dict
		self.key = match_dict["key"].encode('ascii', 'ignore')
		self.level = match_dict["comp_level"]
		self.match_num = match_dict["match_number"]
		self.bad = False
		if str(match_dict["score_breakdown"]) == "None":
			self.bad = True
			return 
		self.blue_alliance_performance = match_dict["score_breakdown"]["blue"]
		self.red_alliance_performance = match_dict["score_breakdown"]["red"]

	def is_bad(self):
		return self.bad

	def get_key(self):
		return self.key

	def get_level(self):
		return self.level

	def get_match_num(self):
		return self.match_num

	def get_totals(self):
		return self.blue_alliance_performance["totalPoints"], self.red_alliance_performance["totalPoints"]

	def get_takeoffs(self):
		blue_takeoffs = 0
		red_takeoffs = 0
		if self.blue_alliance_performance["touchpadNear"] == "ReadyForTakeoff":
			blue_takeoffs += 1
		if self.red_alliance_performance["touchpadNear"] == "ReadyForTakeoff":
			red_takeoffs += 1
		if self.blue_alliance_performance["touchpadMiddle"] == "ReadyForTakeoff":
			blue_takeoffs += 1
		if self.red_alliance_performance["touchpadMiddle"] == "ReadyForTakeoff":
			red_takeoffs += 1
		if self.blue_alliance_performance["touchpadFar"] == "ReadyForTakeoff":
			blue_takeoffs += 1
		if self.red_alliance_performance["touchpadFar"] == "ReadyForTakeoff":
			red_takeoffs += 1
		return blue_takeoffs, red_takeoffs