"""
A most-basic use of the SendGrid email-sending APIs (using their Python module) to sent water-notifications
See this page for more-and-better use of the `sendgrid` module: https://github.com/sendgrid/sendgrid-python
"""

import datetime
import os
import RPi.GPIO as GPIO
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Variables used below
sendgrid_api_key = os.environ.get('SENDGRID_API_KEY') 
from_email = os.environ['WATER_FROM_EMAIL']
to_email = os.environ['WATER_TO_EMAIL']
last_send_filename = '/tmp/last_sent_email.txt'
debounce_in_seconds = 300  # 5 minutes


def send_email_message(incoming_pin): 
	"""Send an Email message if one has not been sent in the last debounce_in_seconds"""

	# Exit early if the `incoming_pin` value is not the water-is-present value
	if os.environ['on_value'] != str(GPIO.input(incoming_pin)):
		return

	now = int(datetime.datetime.now(tz=datetime.timezone.utc).timestamp())

	if not os.path.exists(last_send_filename):
		with open(last_send_filename, 'w') as handle:
		   result = handle.write(str(now - debounce_in_seconds - 10))

	with open(last_send_filename, 'r') as handle:
		last_run = int(handle.read())

	if last_run + debounce_in_seconds > now:
		print(
			f"Logging Email Message: Not sending message as one was already sent {now - last_run} seconds ago. Must wait "
			f"at least {debounce_in_seconds} seconds."
		)
		return

	message = Mail(
		from_email=from_email,
		to_emails=to_email,
		subject='There is water in your house!!',
		html_content=f'<strong>There is water in your house at location {incoming_pin}</strong>'
	)

	try:
		sg = SendGridAPIClient(sendgrid_api_key)
		response = sg.send(message)
		print(f"Logging Email Message: Success for incoming_pin {incoming_pin}:")
		print(f"\tStatus Code: {response.status_code}")
		print(f"\tBody: {response.body}")
		print(f"\tHeaders: {response.headers}")
	except Exception as e:
		print(f"Logging Email Message: FAILURE - {e}")

	try:
		with open(last_send_filename, 'w') as handle:
			handle.write(str(now))
	except Exception as e:
		print(
			f"Failure to write to Email Notification log file ({last_send_filename}): "
			f"FAILURE - {e}"
		)
