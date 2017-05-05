from bot_mailchimp import BotMailChimp

mailchimp_bot = BotMailChimp()
campaign = mailchimp_bot.test_campaign_retrieval('Cardiff, United Kingdom [CWL]')
print(campaign)