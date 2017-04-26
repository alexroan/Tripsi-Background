import os, json
from flight_checker import FlightChecker
from flight_classes import SearchParameters

class BotSkyscanner:

	def __init__(self):
		self.browse_api_key = os.environ['SKYSCANNER_BROWSE_KEY']
		self.live_api_key = os.environ['SKYSCANNER_LIVE_KEY']

		self.flight_checker = FlightChecker(browse_key=self.browse_api_key, 
			live_key=self.live_api_key, market='UK', currency='GBP', locale='en-GB')

		self.destination='Anywhere'  
		self.dept_day=4
		self.earliest_dept_time='16:00'
		self.latest_dept_time='23:30'
		self.ret_day=6
		self.earliest_ret_time='10:00'
		self.latest_ret_time='23:30'
		self.max_price_pp=60.0
		self.adults=1
		self.weeks_ahead=8

	#takes a list of keys
	def browse_origins(self, origin_keys):
		origin_results = {}
		for origin_key in origin_keys:
			origin = self.parse_origin_key(origin_key)
			if origin is None:
				print('origin is none, moving to next')
				continue
			search_params = SearchParameters(origin=origin,
                                 destination=self.destination,
                                 max_price_pp=self.max_price_pp,
                                 weekly_departure_day=self.dept_day,
                                 weekly_return_day=self.ret_day,
                                 weeks_ahead=self.weeks_ahead,
                                 earliest_dept_time=self.earliest_dept_time,
                                 latest_dept_time=self.latest_dept_time,
                                 earliest_ret_time=self.earliest_ret_time,
                                 latest_ret_time=self.latest_ret_time,
                                 adults=self.adults)
			browse_results = self.flight_checker.browse_cache_by_route(search_params)
			print(json.dumps(browse_results))


	#use raw input from mailchimp origin and try to obtain
	#its skyscanner code e.g. 'CWL'
	def parse_origin_key(self, origin_key):
		if '[' in origin_key and ']' in origin_key:
			split_1 = origin_key.split('[')
			if len(split_1) > 1:
				split_2 = split_1[1].split(']')
				return split_2[0]
		return None