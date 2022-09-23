"""
Just a simple class, used as a static-method (really), to demonstrate another approach to triggering a notification
"""

import os
import RPi.GPIO as GPIO


class AltMessage:
	"""Logs which pin is triggering this class"""
	def __call__(self, incoming_pin):
		value = str(GPIO.input(incoming_pin))
		if os.environ['on_value'] == value:
			print(f"AltMessage Log: Incoming Pin = {incoming_pin} -- it's value is {value}")

