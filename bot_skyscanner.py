from bot_mailchimp import BotMailChimp

chimp = BotMailChimp()
origins = chimp.get_origins_subscriptions()

if origins is None:
	print('Exiting')
	quit()
