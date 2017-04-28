from bot_mailchimp import BotMailChimp
from bot_skyscanner import BotSkyscanner

chimp = BotMailChimp()
origins = chimp.get_origins_subscriptions()
print(origins)
if origins is None:
	print('Exiting')
	quit()

scanner = BotSkyscanner()
browse_results = scanner.browse_origins(origins)
for result_origin in browse_results:
	print('Results for origin: %s' % result_origin)
	for advancha in browse_results[result_origin]:
		print(advancha.basic_str())
		print("Getting live pricing information...")
		scanner.live_pricing(advancha)
		
