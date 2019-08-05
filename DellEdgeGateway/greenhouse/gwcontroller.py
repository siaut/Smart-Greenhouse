#!/usr/bin/env python

import time
import datetime
import pytz
import requests
import sys

while True:
    utc = pytz.utc
    loc_dt = utc.localize(datetime.datetime.today().replace(hour=7, minute=0))
    loc_dt2 = utc.localize(datetime.datetime.today().replace(hour=21, minute=0))
    today = utc.localize(datetime.datetime.today())
    #API_EndPointLight = "http://172.16.254.60:5000/led?switch="
    API_EndPointLight = "http://192.168.204.191:5000/led?switch="
		
    print "loc_dt "
    print loc_dt
    print "loc_dt2 " 
    print loc_dt2
    print "today " 
    print today
    try:
        if (loc_dt < today) and (loc_dt2 > today):
	    	# switch on light from 7 am to 9pm
            print "switch on light after 7am"
            #lightState = 1
            result = requests.post(API_EndPointLight+"on")
        else:
            # switch off light after 9 pm
            print "switch off light after 9 pm"
            #lightState = 1
            result = requests.post(API_EndPointLight+"off")
    except:
        e = sys.exc_info()[0]
        print e
	
    time.sleep(300) # wait 5 min		




    





