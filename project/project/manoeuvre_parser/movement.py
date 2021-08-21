# movement.py Copyright (C) 2019 Douglas Inglis
# Simple class which defines functions for moving the robot in a specified direction with the attached L298N motor controller

import sys
import time
import RPi.GPIO as GPIO

# Define pins used to control motor controller

MOTOR_1_FORWARD_PIN = 15
MOTOR_1_BACKWARD_PIN = 18

MOTOR_2_FORWARD_PIN = 14
MOTOR_2_BACKWARD_PIN = 2

class Movement:
	def __init__(self):
		pass
		GPIO.setwarnings(False) # Disable spurious warnings
		GPIO.setmode(GPIO.BCM) # Set GPIO pin numbering to Broadcom
		
		# Setup all relevent pins as outputs

		GPIO.setup(MOTOR_1_FORWARD_PIN, GPIO.OUT) 
		GPIO.setup(MOTOR_1_BACKWARD_PIN, GPIO.OUT)
		GPIO.setup(MOTOR_2_FORWARD_PIN, GPIO.OUT)
		GPIO.setup(MOTOR_2_BACKWARD_PIN, GPIO.OUT)	

	def forward(self, t):
		# Set the pins to high
		GPIO.output(MOTOR_1_FORWARD_PIN, GPIO.HIGH)
		GPIO.output(MOTOR_2_FORWARD_PIN, GPIO.HIGH)
		print("Moving forward for {} seconds.".format(t))
		time.sleep(t) # Sleep for however long the movement will last
		# Set the pins to low
		GPIO.output(MOTOR_1_FORWARD_PIN, GPIO.LOW)
		GPIO.output(MOTOR_2_FORWARD_PIN, GPIO.LOW)	

	def backward(self, t):
		# Set the pins to high
		GPIO.output(MOTOR_1_BACKWARD_PIN, GPIO.HIGH)
		GPIO.output(MOTOR_2_BACKWARD_PIN, GPIO.HIGH)
		print("Moving backward for {} seconds.".format(t))
		time.sleep(t) # Sleep for however long the movement will last
		# Set the pins to low
		GPIO.output(MOTOR_1_BACKWARD_PIN, GPIO.LOW)
		GPIO.output(MOTOR_2_BACKWARD_PIN, GPIO.LOW)

	def right(self, t):
		# Set the pins to high
		GPIO.output(MOTOR_1_FORWARD_PIN, GPIO.HIGH)
		GPIO.output(MOTOR_2_BACKWARD_PIN, GPIO.HIGH)
		print("Moving right for {} seconds.".format(t))
		time.sleep(t) # Sleep for however long the movement will last
		# Set the pins to low
		GPIO.output(MOTOR_1_FORWARD_PIN, GPIO.LOW)
		GPIO.output(MOTOR_2_BACKWARD_PIN, GPIO.LOW)

	def left(self, t):
		# Set the pins to high
		GPIO.output(MOTOR_1_BACKWARD_PIN, GPIO.HIGH)
		GPIO.output(MOTOR_2_FORWARD_PIN, GPIO.HIGH)
		print("Moving left for {} seconds.".format(t))
		time.sleep(t) # Sleep for however long the movement will last
		# Set the pins to low
		GPIO.output(MOTOR_1_BACKWARD_PIN, GPIO.LOW)
		GPIO.output(MOTOR_2_FORWARD_PIN, GPIO.LOW)
