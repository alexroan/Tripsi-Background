import sendgrid
import os
from sendgrid.helpers.mail import *

class EmailSender:

	def __init__(self):
		self.sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
		
	
	def send_email(self, email, title, content):
		from_email = Email(os.environ.get('TRIPSI_EMAIL'), "Tripsi")
		subject = title
		to_email = Email(email)
		content = Content("text/html", content)
		mail = Mail(from_email, subject, to_email, content)
		response = self.sg.client.mail.send.post(request_body=mail.get())
		print(response.status_code)
		print(response.body)
		print(response.headers)