from bot_mailchimp import BotMailChimp
from bot_skyscanner import BotSkyscanner
import time, json

chimp = BotMailChimp()
origins = chimp.get_origins_subscriptions()
print(json.dumps(origins))
if origins is None:
	print('Exiting')
	quit()

advenchas = []
scanner = BotSkyscanner()

for airport in origins:
	for currency in origins[airport]:
		advenchas = scanner.browse_origin(airport, currency)
		print('Results for %s in %s' % (airport, currency))
		if advenchas is not None:
			for advencha in advenchas:
				print(advencha.basic_str())

