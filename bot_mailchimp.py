import os, json
from mailchimp3 import MailChimp

class BotMailChimp:

	def __init__(self):
		self.api_key = os.environ['MAILCHIMP_API_KEY']
		#start client
		self.client = MailChimp('alexroan', self.api_key)
	
	def get_origins_subscriptions(self):
		
		all_lists = self.client.lists.all(get_all=True, fields="lists.name,lists.id")

		#find the subscriptions lit
		list_id = None
		for li in all_lists['lists']:
			if li['name'] == 'Subscriptions':
				list_id = li['id']
		#exit if not found
		if list_id is None:
			print('could not get subscription lits id')
			return None

		#get origins and assign them as key in origins_emails
		#value of each key is list of email associated with that origin
		origins_emails = {}
		members = self.client.lists.members.all(li['id'], get_all=True)
		for member in members['members']:
			if(member['status'] == 'subscribed'):
				email_address = member['email_address']
				origin_airport = member['merge_fields']['ORIGIN']
				if origin_airport not in origins_emails:
					origins_emails[origin_airport] = [email_address]
				else:
					origins_emails[origin_airport].append(email_address)
		return origins_emails


	