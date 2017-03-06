import urllib2
import json

def get_event_list():
	url = "http://www.thebluealliance.com/api/v2/events/2017" + '?X-TBA-App-Id=frc8%3Asteamworks-takeoff-analysis%3Atest'
	request = urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'})
	data = urllib2.urlopen(request).read().decode('utf-8')
	jsonvar = json.loads(data)

	return_val = []
	for i in jsonvar:
		return_val.append(sEvent(i))
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
		self.blue_alliance_performance = match_dict["score_breakdown"]["blue"]
		self.red_alliance_performance = match_dict["score_breakdown"]["red"]

		def get_key(self):
			return self.key

		def get_level(self):
			return self.level

		def get_match_num(self):
			return self.match_num

		def get_totals(self):
			return self.blue_alliance_performance["totalPoints"], self.red_alliance_performance["totalPoints"]

		def get_takeoffs(self):
			blue_takeoffs = self.blue_alliance_performance["teleopTakeoffPoints"]
			red_takeoffs = self.red_alliance_performance["teleopTakeoffPoints"]
			return blue_takeoffs, red_takeoffs