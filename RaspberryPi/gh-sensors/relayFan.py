#!/usr/bin/env python

import RPi.GPIO as GPIO
#time and json
import time
import json

# setting a list of used pins 
#pins = [5,6,13,19]

# setting GPIO mode
GPIO.setmode(GPIO.BCM) # number pins by GPIO 
GPIO.setwarnings(False)

GPIO.setup(13,GPIO.OUT)

GPIO.output(13,  GPIO.LOW)
time.sleep(5)



GPIO.cleanup()
