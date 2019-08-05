#!/usr/bin/env python

#import time
import os, sys
import json
import redis
import urlparse
import requests
import urllib2
import flask_sijax
import datetime
import pytz

from requests.auth import HTTPDigestAuth


from random import random
from time import time
from flask import Flask, abort, request ,render_template, make_response,g

path = os.path.join('.', os.path.dirname(__file__), '../')
sys.path.append(path)

#from flask import Flask, g, render_template

app = Flask(__name__)

# The path where you want the extension to create the needed javascript files
# DON'T put any of your files in this directory, because they'll be deleted!
app.config["SIJAX_STATIC_PATH"] = os.path.join('.', os.path.dirname(__file__), 'static/js/sijax/')

# You need to point Sijax to the json2.js library if you want to support
# browsers that don't support JSON natively (like IE <= 7)
app.config["SIJAX_JSON_URI"] = '/static/js/sijax/json2.js'

flask_sijax.Sijax(app)

rediscloud_service = json.loads(os.environ['VCAP_SERVICES'])['p.redis'][0]
credentials = rediscloud_service['credentials']
r = redis.Redis(host=credentials['host'], port=credentials['port'], password=credentials['password'])
weatherkey= str(os.environ.get('weatherkey'))
mapkey1= str(os.environ.get('mapkey'))

def checkWeather():
	#f = urllib2.urlopen("http://api.wunderground.com/api/"+ weatherkey + #"/geolookup/conditions/q/Singapore/Singapore.json")
	#json_string = f.read()
	#parsed_json = json.loads(json_string)
	#location = parsed_json['location']['city']
	location = "Singapore"
	temp_c = "30"
	#temp_c = parsed_json['current_observation']['temp_c']
	#print json.dumps(parsed_json, sort_keys=True, indent=4)
	message= "Temperature:" + str(temp_c)
	#UV = parsed_json['current_observation']['UV']
	UV = "fair"
	print "UV:" + UV
	message = message + "<br>"+ "UV: "+ UV
	#icon= parsed_json['current_observation']['icon']
	icon = ""
	#print icon
	message = message + "<br>" + icon
	#icon_url= parsed_json['current_observation']['icon_url']
	icon_url = ""
	#print icon_url
	#relative_humidity= parsed_json['current_observation']['relative_humidity']
	relative_humidity = "66%"
	print "Relative Humidity:" + relative_humidity
	message = message + "<br>" + "Relative Humidity: " + str(relative_humidity)

	#f.close()
	r.set('weathermessage',message)
	r.set('iconurl',icon_url)
	

def comet_do_work_handler(obj_response):
    wtimer=int(r.get('weathertimer'))
    print "wtimer:" + str(wtimer)
    if wtimer==1:
        checkWeather()
        wtimer=wtimer+1
    elif wtimer==6:        
        wtimer=1
    else:
        wtimer=wtimer+1
        
    r.set('weathertimer',str(wtimer))

        #width = '%spx' % (i * 80)
        #obj_response.css('#progress', 'width', width)
    obj_response.html('#timevalue', 'Time:'+str(r.get('timevalue')))
    obj_response.html('#lightvalue', 'Light:'+str(r.get('lightvalue')))
    obj_response.html('#tempvalue', 'Temperature:'+str(r.get('tempvalue')))
    obj_response.html('#moisvalue', 'Soil Moisture:'+str(r.get('moisvalue')))	
    obj_response.html('#weathervalue', str(r.get('weathermessage')))
    #print 'Distance: %0.2f m' %d
    awsbaseurl='http://iotcamera01.demo1.ecs1.sgcloud.com:9020/'+str(r.get('alertsnapshotfilename'))
    snapshoturl="<img src=\"" +awsbaseurl + "\" height=300 width=360 />"	
    obj_response.html('#alertphotovalue', snapshoturl)

    if r.get('alertcam')=='0': #remote demo cam 2
        obj_response.html('#alertvalue',"<span class=\"blinking\">Camera 2: Intruder Alert! <br>Distance:"+ '%0.2f m'%float(r.get('alertdistancevalue'))+ "<br>Time:"+str(r.get('alerttimevalue')) +" <br><br>"+ str(r.get('alertmessage')).replace(";","<br>") +"</span>")	
    else: # cam 1 
        obj_response.html('#alertvalue',"<span class=\"blinking\">Camera 1: Intruder Alert! <br>Distance:"+ '%0.2f m'%float(r.get('alertdistancevalue'))+ "<br>Time:"+str(r.get('alerttimevalue')) +" <br><br>"+ str(r.get('alertmessage')).replace(";","<br>") +"</span>")
	
    #obj_response.html('#weathericon', str(r.get('iconurl')))
    # Yielding tells Sijax to flush the data to the browser.
    # This only works for Streaming functions (Comet or Upload)
    # and would not work for normal Sijax functions
    yield obj_response

def toggle_led_switch():
    if r.get('ledswitch') == "off":
        r.set('ledswitch',"on")
    elif r.get('ledswitch') == "on":
        r.set('ledswitch',"off")

def toggle_fan_switch():
    if r.get('fanswitch') == "off":
        r.set('fanswitch',"on")
    elif r.get('fanswitch') == "on":
        r.set('fanswitch',"off")

def toggle_cloud_switch():
    if r.get('cloudswitch') == "off":
        r.set('cloudswitch',"on")
    elif r.get('cloudswitch') == "on":
        r.set('cloudswitch',"off")   
		
def comet_do_switchLed_handler(obj_response):
    # defining the api-endpoint 
	toggle_led_switch()
	API_EndPointLED = "http://10.36.67.144:5000/led?switch="+str(r.get('ledswitch'))
	result = requests.post(API_EndPointLED)

def comet_do_switchFan_handler(obj_response):
    # defining the api-endpoint 
	toggle_fan_switch()
	API_EndPointLED = "http://10.36.67.144:5000/fan?switch="+str(r.get('fanswitch'))
	result = requests.post(API_EndPointLED)

def comet_do_switchCloud_handler(obj_response):
    # defining the api-endpoint 
	print obj_response
	toggle_cloud_switch()
	API_EndPointLED = "http://172.24.4.58:5000/cloud?switch="+str(r.get('cloudswitch'))
	result = requests.post(API_EndPointLED)
	
@app.route('/live-data') 
def live_data():
    # Create an array and echo it as JSON
    utc_now = pytz.utc.localize(datetime.datetime.utcnow())
    pst_now = utc_now.astimezone(pytz.timezone("Asia/Seoul"))
    epoch2 = datetime.datetime(1970,1,1, tzinfo=pytz.timezone("Asia/Seoul"))
    ts = (pst_now - epoch2).total_seconds()
	
    data=[ts*1000,int(r.get('lightvalue'))]

    print "live-data:" + str(data)
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response

@app.route('/live-data2') 
def live_data2():
    utc_now = pytz.utc.localize(datetime.datetime.utcnow())
    pst_now = utc_now.astimezone(pytz.timezone("Asia/Seoul"))
    epoch2 = datetime.datetime(1970,1,1, tzinfo=pytz.timezone("Asia/Seoul"))
    ts = (pst_now - epoch2).total_seconds()
	
    data=[ts*1000,float(r.get('tempvalue')) ]
	
    print "live-data2:" + str(data)
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response

@app.route('/live-data3') 
def live_data3():
    utc_now = pytz.utc.localize(datetime.datetime.utcnow())
    pst_now = utc_now.astimezone(pytz.timezone("Asia/Seoul"))
    epoch2 = datetime.datetime(1970,1,1, tzinfo=pytz.timezone("Asia/Seoul"))
    ts = (pst_now - epoch2).total_seconds()
	
    data=[ts*1000,float(r.get('moisvalue')) ]
	
    print "live-data3:" + str(data)
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response

@flask_sijax.route(app, "/")
def index():
    #AXIS_CAMERA_URL='https://172.24.4.71'
    #response = requests.get(AXIS_CAMERA_URL, auth=HTTPDigestAuth('root', 'pass'))

    if g.sijax.is_sijax_request:
        # The request looks like a valid Sijax request
        # Let's register the handlers and tell Sijax to process it
        g.sijax.register_comet_callback('do_work', comet_do_work_handler)
        g.sijax.register_comet_callback('do_switchLed', comet_do_switchLed_handler)
        g.sijax.register_comet_callback('do_switchFan', comet_do_switchFan_handler)
        g.sijax.register_comet_callback('do_switchCloud', comet_do_switchCloud_handler)
        return g.sijax.process_request()
    
    #return render_template('index.html', data='test')
    return render_template('index.html',mapkey=mapkey1)

@app.route('/sensors', methods=['POST']) 
def sensors():
    sensors = request.args.get("sensors")
    sensorslist=sensors.split(",")
    r.set('timevalue',sensorslist[0])
    r.set('tempvalue',sensorslist[3])
    r.set('lightvalue',sensorslist[1])
    r.set('moisvalue',sensorslist[2])
    print "Time:" + str(sensorslist[0])
    print "Light:" + str(sensorslist[1])
    print "Moisture:" + str(sensorslist[2])
    print "Temperature:" + str(sensorslist[3])
    #+ " light:" + r.get('lightvalue')
    return "sensors:" + str(sensors)



if __name__ == "__main__":
	if r.exists('ledswitch') !=1:
		r.set('ledswitch',"off")
	r.set('fanswitch',"off")
	r.set('cloudswitch',"off")
	r.set('weathertimer',"1")
	r.set('weathermessage',"")
	r.set('iconurl',"")
	app.run(debug=False,host='0.0.0.0', port=int(os.getenv('PORT', '5000')))
    
