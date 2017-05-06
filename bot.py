from bot_mailchimp import BotMailChimp
from bot_skyscanner import BotSkyscanner
from bot_email_parser import BotEmailParser
import time, json, io

chimp = BotMailChimp()
origins = chimp.get_origins_subscriptions()
print(json.dumps(origins))
if origins is None:
	print('Exiting')
	quit()

advenchas = []
scanner = BotSkyscanner()

email_parser = BotEmailParser('templates/email_template.html')
skyscanner_api_key_16 = scanner.browse_api_key[:16]

for airport in origins:
	for currency in origins[airport]:
		advenchas = scanner.browse_origin(airport, currency)
		if advenchas is not None:
			email_result = email_parser.construct_email(airport, currency, advenchas, skyscanner_api_key_16)
			file = open('emails/%s%s.html' % (airport, currency), "w")
			file.write(email_result.decode("utf-8"))
			file.close()
		else:
			print('advenchas is none')

"""
		print('Results for %s in %s' % (airport, currency))
		if advenchas is not None:
			for advencha in advenchas:
				print(advencha.basic_str())
"""

