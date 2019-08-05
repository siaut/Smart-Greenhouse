#!/usr/bin/env python

import RPi.GPIO as GPIO
#time and json
import time
import json

# setting a list of used pins 
#pins = [5,6,13,19]

# setting GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(19,GPIO.OUT)

GPIO.output(19,  GPIO.HIGH)
time.sleep(0.5)
GPIO.output(19,  GPIO.LOW)
time.sleep(0.5)
GPIO.output(19,  GPIO.HIGH)
time.sleep(0.5)


GPIO.cleanup()
