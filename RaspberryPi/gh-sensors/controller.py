#!/usr/bin/env python
import ADC0832_tmp
import time
import os
import subprocess
import RPi.GPIO as GPIO
from flask import Flask, abort, request 
import json

app_path='/root/iot/gh-sensors/'
app = Flask(__name__)

LedPin = 15    # pin15
FanPin = 33 # Fan
MainLightPin = 35 # Main Light
MainLightStatus = 2

def setup():
	ADC0832_tmp.setup()
	GPIO.setmode(GPIO.BOARD)       # Numbers pins by physical location
	GPIO.setwarnings(False)
	GPIO.setup(LedPin, GPIO.OUT)   # Set pin mode as output
	GPIO.setup(FanPin,GPIO.OUT)
	GPIO.setup(MainLightPin,GPIO.OUT)
	GPIO.output(LedPin, GPIO.LOW) # Set pin to high(+3.3V) to off the led

	#print subprocess.check_output(['/root/iot/hub-ctrl','-h','0','-P','2','-p','0'])

def destroy():
	# let startsensors destroy ADC.
	#ADC0832_tmp.destroy()
	#print subprocess.check_output(['/root/iot/hub-ctrl','-h','0','-P','2','-p','0'])
	GPIO.output(LedPin, GPIO.HIGH)     # led off
	GPIO.output(FanPin,  GPIO.HIGH)		# Fan off
	GPIO.cleanup()                     # Release resource
	print(" - I have run the cleanup function -")

def MainLight(state):
	global MainLightStatus
	if state == 0:
		if MainLightStatus ==1:
			toggleMainLight()
			toggleMainLight()
		elif MainLightStatus ==2:
			toggleMainLight()
	elif state ==1:
		if MainLightStatus ==0:
			toggleMainLight()
		elif MainLightStatus ==2:
			toggleMainLight()
			toggleMainLight()
	elif state ==2:
		if MainLightStatus==0:
			toggleMainLight()
			toggleMainLight()
		elif MainLightStatus==1:
			toggleMainLight()
	MainLightStatus = state

def toggleMainLight():
	GPIO.output(MainLightPin,  GPIO.HIGH)
	time.sleep(0.5)
	GPIO.output(MainLightPin,  GPIO.LOW)
	time.sleep(0.5)
	GPIO.output(MainLightPin,  GPIO.HIGH)
	time.sleep(0.5)

def speakfromRecording(filename):
    subprocess.call(["/usr/bin/omxplayer",filename])
	
def speakBoth():
	speakfromRecording(app_path+'english.mp3')
	speakfromRecording(app_path+'japanese.mp3')
	
@app.route('/')
def mainmenu():

    return """
    <html><body>
    
    </body></html>
    """.format("")

@app.route('/speak', methods=['POST']) 
def speak():
    switch = request.args.get("switch")
    if switch == "on":
        speakBoth()
        print '...speaker'
		
    return switch
	
@app.route('/led', methods=['POST']) 
def led():
    switch = request.args.get("switch")
    if switch == "on":
        GPIO.output(LedPin, GPIO.HIGH)  # led on
        MainLight(2)
        print '...led on'
    else:
        GPIO.output(LedPin, GPIO.LOW) # led off
        MainLight(0)
        print '...led off'
		
    return switch

@app.route('/fan', methods=['POST']) 
def fan():
    switch = request.args.get("switch")
    if switch == "on":
        #print subprocess.check_output(['/root/iot/hub-ctrl','-h','0','-P','2','-p','1'])
        GPIO.output(FanPin,  GPIO.LOW)  # fan on
        print '...fan on'
    else:
        #print subprocess.check_output(['/root/iot/hub-ctrl','-h','0','-P','2','-p','0'])
        GPIO.output(FanPin,  GPIO.HIGH) # fan off
        print '...fan off'
		
    return switch



if __name__ == "__main__":

    setup()
    try:
        app.run(debug=False,host='0.0.0.0', port=int(os.getenv('PORT', '5000')))
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()

