#!/usr/bin/env python
import sys

sys.path.insert(0,'/root/iot/gh-sensors')

import ADC0832_tmp
import RPi.GPIO as GPIO

import os
import time
import paho.mqtt.client as mqtt
import datetime
import subprocess

broker_address="192.168.204.192"

LedPin = 15    # pin15
FanPin = 33 # Fan
MainLightPin = 35 # Main Light
MainLightStatus = 2

g_temperature=0

print("creating new instance")
client = mqtt.Client("pub5") #create new instance

print("connecting to broker")
client.connect(broker_address,port=1883) #connect to broker ,old port=31881
#client.connect(broker_address,port=31881) #connect to broker ,old port=31881

# Reads temperature from sensor 
# id is the id of the sensor
def readSensor(id):
    global g_temperature
    currenttime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    tfile = open("/sys/bus/w1/devices/"+id+"/w1_slave")
    text = tfile.read()
    tfile.close()
    secondline = text.split("\n")[1]
    temperaturedata = secondline.split(" ")[9]
    temperature = float(temperaturedata[2:])
    g_temperature = temperature / 1000
    #print "Sensor: " + id  + " - Temperature : %0.3f C" % temperature
    #print "Temperature : %0.3f C" % g_temperature
    #client.publish("temperature",currenttime + "," + str(g_temperature))


# Reads temperature from all sensors found in /sys/bus/w1/devices/
# starting with "28-...
def readSensors():
    count = 0
    sensor = ""
    for file in os.listdir("/sys/bus/w1/devices/"):
        if (file.startswith("28-")):
            readSensor(file)
            count+=1
    if (count == 0):
        print "No sensor found! Check connection"

def init():
	ADC0832_tmp.setup()
	GPIO.setmode(GPIO.BOARD)       # Numbers pins by physical location
	GPIO.setwarnings(False)
	GPIO.setup(LedPin, GPIO.OUT)   # Set pin mode as output
	GPIO.setup(FanPin,GPIO.OUT)
	GPIO.setup(MainLightPin,GPIO.OUT)
	GPIO.output(LedPin, GPIO.LOW) # Set pin to high(+3.3V) to off the led
	
	
def speakfromRecording(filename):
    subprocess.call(["/usr/bin/omxplayer",filename])
	
def speakBoth():
	speakfromRecording('english.mp3')
	speakfromRecording('japanese.mp3')
	
def loop():
    while True:
        currenttime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        res = ADC0832_tmp.getResult() - 80
        if res < 0:
            res = 0
        if res > 100:
            res = 100
        print "Time: " + currenttime
        print 'Sunlight = %d' % res
        res1 = ADC0832_tmp.getResult1()
        moisture = 255 - res1
        print 'Soil moisture: %d' %(moisture)
        readSensors()
        print "G Temperature : %0.3f C" % g_temperature
        distance = ADC0832_tmp.checkdist()
        print 'Distance: %0.2f m' % distance

		
		
        client.publish("sensors",currenttime + "," + str(res)+","+str(moisture)+","+str(g_temperature)+","+str(distance))
        time.sleep(5)

# Nothing to cleanup
def destroy():
    pass
	
if __name__ == '__main__':
    init()
    try:
        loop()
    except KeyboardInterrupt: 
        ADC0832_tmp.destroy()
        destroy()
        print 'The end !'
