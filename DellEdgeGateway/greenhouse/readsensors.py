#!/usr/bin/env python

import paho.mqtt.client as mqtt
import time
import datetime
import pytz
import requests
import AxisCamera
import vision
import TensorVision
from SimpleCV import Camera

app_path='/opt/greenhouse/'
file_name='cloudswitch.txt'
image_fname='snapshot.jpg'
API_ENDPOINT = "http://gh-controller.apps.csc-dell.com/sensors"
API_ENDPOINT_ALERT = "http://gh-controller.apps.csc-dell.com/alerts"

def takesnapshotUSB():
	#os.system('fswebcam -r 320x240 -S 3 --jpeg 50 --save /home/pi/to_transmit/%H%M%S.jpg') # uses Fswebcam to take picture
	#os.system('fswebcam -r 640x480 --no-banner --save ' + file_path + file_name) # uses Fswebcam to take picture
    img = cam.getImage()
    img.save(app_path + image_fname)	

def check_cloudswitch():
    cloudswitch="off"
    try:
        file = open(app_path+file_name,'r')
        cloudswitch= file.read()
        print "cloudswitch=" + cloudswitch
    finally:
        file.close()
		
    return cloudswitch
			

def on_message(client, userdata, message):
    #global lightState
    m = str(message.payload.decode("utf-8"))
    list = m.split(",")
    print("Distance: " + str(list[4]))
    if float(list[4]) < 0.2:

        print "***Intruder Alert***"
        API_EndPointSpeak = "http://192.168.204.191:5000/speak?switch=on"
        #API_EndPointSpeak = "http://10.36.67.144:5000/speak?switch=on"
		
        result = requests.post(API_EndPointSpeak)
        print( "result:" + str(result))	
	
        #AxisCamera.takesnapshot()
        #AxisCamera.takesnapshotUSB()
        takesnapshotUSB()
        filename=AxisCamera.uploadToECS()
        cloudswitch=check_cloudswitch()
        if cloudswitch=="on":
		    AxisCamera.uploadToAWS(filename)
		    vresp = vision.MSvision()
        else:
		    vresp = TensorVision.Tvision()        
        print vresp
        PARAMS_ALERT = {'sensors':m,'filename':filename,'alerts':vresp} 
        r2 = requests.post(url = API_ENDPOINT_ALERT, params = PARAMS_ALERT, verify=False)
		
    print("Sensors: " + m)    
    PARAMS = {'sensors':m}   	
    r = requests.post(url = API_ENDPOINT, params = PARAMS, verify=False)
    #requests.api.request('post', API_ENDPOINT, data=PARAMS, json=None, verify=False)
    #pastebin_url = r.text
    #print pastebin_url


broker_address="192.168.204.192"
print("creating new instance")
client = mqtt.Client("readsensor") #create new instance
client.on_message=on_message #attach function to callback
print("connecting to broker")
client.connect(broker_address,port=1883) #connect to broker

cam = Camera()
time.sleep(0.1)  # Wait for initialization	
client.loop_start() #start the loop

while True:
    client.subscribe("sensors")
    time.sleep(5) # wait

client.loop_stop() #stop the loop


