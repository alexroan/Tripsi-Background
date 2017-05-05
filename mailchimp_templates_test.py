from bot_mailchimp import BotMailChimp
import os, json

template_id = os.environ['MAILCHIMP_TEMPLATE_ID']

mailchimp_bot = BotMailChimp()
print(json.dumps(mailchimp_bot.get_email_template(template_id)))