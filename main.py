import time
import os
import RPi.GPIO as GPIO
from alt_msg import AltMessage
from send_email_notification import send_email_message
from send_sms_notification import send_sms_message

pin = int(os.environ['pin'])  # Setting `pin` for ease-of-use below 
os.environ['on_value'] = "0"  # Set this for YOUR setup!!


def pin_activated(activated_pin):
    incoming_value = GPIO.input(activated_pin)
    if os.environ['on_value'] == incoming_value:
        print(f"pin_activated Log: Activated pin = {activated_pin} - Value = {incoming_value}")

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(pin, GPIO.IN)

GPIO.add_event_detect(pin, GPIO.BOTH, bouncetime=300)
GPIO.add_event_callback(pin, pin_activated)
GPIO.add_event_callback(pin, AltMessage())
GPIO.add_event_callback(pin, send_email_message)
GPIO.add_event_callback(pin, send_sms_message)


print(f"Current value of pin: {GPIO.input(pin)}\n")

while True:
	time.sleep(60)

