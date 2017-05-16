from bot_mailchimp import BotMailChimp
from bot_skyscanner import BotSkyscanner
from bot_email_parser import BotEmailParser
from bot_sendgrid import EmailSender
import time, json, io, os

chimp = BotMailChimp()
origins = chimp.get_origins_subscriptions()
print(json.dumps(origins))
if origins is None:
	print('Exiting')
	quit()

advenchas = []
scanner = BotSkyscanner()

email_parser = BotEmailParser('templates/email_template.html')
email_sender = EmailSender()
skyscanner_api_key_16 = scanner.live_api_key[:16]

origins_not_processed = []

for airport in origins:
	for currency in origins[airport]:
		advenchas = scanner.browse_origin(airport, currency)
		if advenchas is not None:
			email_result = email_parser.construct_email(airport, currency, advenchas, skyscanner_api_key_16)
			
			#print email to a file
			directory = 'emails'
			if not os.path.exists(directory):
				os.makedirs(directory)
			file = open('%s/%s%s.html' % (directory, airport, currency), "w")
			file.write(email_result.decode("utf-8"))
			file.close()
			
			for email_address in origins[airport][currency]:
				#send email to test address
				email_sender.send_email(email_address, "Flights From %s" % airport, email_result.decode("utf-8"))
			
		else:
			origins_not_processed.append([airport, currency])

print('Origins not processed: %s' % str(origins_not_processed))