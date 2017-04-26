from bot_mailchimp import BotMailChimp
from bot_skyscanner import BotSkyscanner

chimp = BotMailChimp()
origins = chimp.get_origins_subscriptions()
print(origins)
if origins is None:
	print('Exiting')
	quit()

scanner = BotSkyscanner()
origin_keys = ['Cardiff [CWL]']
scanner.browse_origins(origin_keys)