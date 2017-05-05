from bot_mailchimp import BotMailChimp
from bot_skyscanner import BotSkyscanner
import time

chimp = BotMailChimp()
origins = chimp.get_origins_subscriptions()
print(origins)
if origins is None:
	print('Exiting')
	quit()

advenchas = []
scanner = BotSkyscanner()
browse_results = scanner.browse_origins(origins)

#TODO - INSTEAD OF BELOW...
#for each origin item, use key to get advenchas from browse_results
#then, using the user details, send links with advencha details to each
#INSTEAD OF BELOW...
for result_origin in browse_results:
	print('Cache browse results for origin: %s' % result_origin)
	for advancha in browse_results[result_origin]:
		print(advancha.basic_str())
		advenchas.append(advancha)




#Live approach not needed for now. Use browse results with referral links to take to skyscanner page first
'''
print('Gathered cache results. Now attempting to retrieve live data...')
for advencha in advenchas:
	print('Sleeping...')
	time.sleep(10)
	print('Awake. Retrieving results for %s' % advencha.basic_str())
	result = scanner.live_pricing(advencha)
	print('Parsing result...')
	parsed_result = scanner.parse_live_price(result)
	print('Live Pricing:')
	for itinerary in parsed_result:
		print(itinerary.basic_str())
'''
