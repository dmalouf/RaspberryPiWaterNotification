"""
A most-basic use of the Twilio SMS API (using their Python module) to sent water-notifications
See this page for more-and-better use of the `twilio` module: https://www.twilio.com/docs/libraries/python
"""

import datetime
import os
import time
import RPi.GPIO as GPIO
from twilio.rest import Client

# Variables used below
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
from_phone = os.environ['TWILIO_FROM_PHONE_NUMBER']
to_phone = os.environ['WATER_TO_PHONE_NUMBER']
last_send_filename = '/tmp/last_sent_sms.txt'
debounce_in_seconds = 300  # 5 minutes

# Initial setup of Twilio client



def send_sms_message(incoming_pin):
	"""Send an SMS message if one has not been sent in the last debounce_in_seconds"""
    
	# Exit early if the `incoming_pin` value is not the water-is-present value
	if os.environ['on_value'] != str(GPIO.input(incoming_pin)):
		return

	now = int(datetime.datetime.now(tz=datetime.timezone.utc).timestamp())

	if not os.path.exists(last_send_filename):
		with open(last_send_filename, 'w') as handle:
			handle.write(str(now - debounce_in_seconds - 10))

	with open(last_send_filename, 'r') as handle:
		last_run = int(handle.read())

	if last_run + debounce_in_seconds > now:
		print(
			f"Logging SMS Message: Not sending message as one was already sent {now - last_run} seconds ago. Must wait "
			f"at least {debounce_in_seconds} seconds."
		)
		return
	
	# Setup client now - ideally this client is not used very often so instantiating it only as-needed should be fine.
	client = Client(account_sid, auth_token)

	message = client.messages.create(
		body='WATER FOUND!! RUN HOME AND FIX IT!',
		from_=from_phone,
		to=to_phone
	)

	print(f"Logging SMS Message: SID = {message.sid}")

	try:
		with open(last_send_filename, 'w') as handle:
			handle.write(str(now))
	except Exception as e:
		print(
			f"Failure to write to SMS Notification log file ({last_send_filename}): "
			f"FAILURE - {e}"
		)
