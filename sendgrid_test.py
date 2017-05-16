import sendgrid
import os
from sendgrid.helpers.mail import *

tripsi_email = os.environ.get('TRIPSI_EMAIL')
test_email = os.environ.get('TEST_EMAIL')

print(tripsi_email, test_email)

sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
from_email = Email(tripsi_email, "Tripsi")
subject = "Hello World from the SendGrid Python Library!"
to_email = Email(test_email, "Alex Roan")
content = Content("text/plain", "Hello, Email!")
mail = Mail(from_email, subject, to_email, content)
response = sg.client.mail.send.post(request_body=mail.get())
print(response.status_code)
print(response.body)
print(response.headers)