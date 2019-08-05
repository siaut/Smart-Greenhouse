#!/usr/bin/env python

import time
import os, sys
from flask import Flask, abort, request, json, g, render_template
import json
import redis
import urlparse
import requests
from flask.ext.mysql import MySQL
import flask_sijax
import pytz
from datetime import datetime, timedelta

local_tz = pytz.timezone('Asia/Singapore') # use your local timezone name here

path = os.path.join('.', os.path.dirname(__file__), '../')
sys.path.append(path)

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

mysql_service = json.loads(os.environ['VCAP_SERVICES'])['p.mysql'][0]
my_sql_credentials = mysql_service['credentials']

mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = my_sql_credentials['username']
print "DB username:" + my_sql_credentials['username']
app.config['MYSQL_DATABASE_PASSWORD'] = my_sql_credentials['password']
app.config['MYSQL_DATABASE_DB'] = my_sql_credentials['name']
app.config['MYSQL_DATABASE_HOST'] = my_sql_credentials['hostname']
mysql.init_app(app)

def utc_to_local(utc_dt):
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt) # .normalize might be unnecessary

def aslocaltimestr(utc_dt):
    return utc_to_local(utc_dt).strftime('%Y-%m-%d %H:%M:%S')
	
def comet_do_work_handler(obj_response):

        #width = '%spx' % (i * 80)
        #obj_response.css('#progress', 'width', width)
    obj_response.html('#timevalue', 'Time:'+str(r.get('timevalue')))
    obj_response.html('#lightvalue', 'Light:'+str(r.get('lightvalue')))
    obj_response.html('#tempvalue', 'Temperature:'+str(r.get('tempvalue')))
    obj_response.html('#moisvalue', 'Soil Moisture:'+str(r.get('moisvalue')))	
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

@flask_sijax.route(app, "/")
def index():
    if g.sijax.is_sijax_request:
        # The request looks like a valid Sijax request
        # Let's register the handlers and tell Sijax to process it
        g.sijax.register_comet_callback('do_work', comet_do_work_handler)
        g.sijax.register_comet_callback('do_switchLed', comet_do_switchLed_handler)
        g.sijax.register_comet_callback('do_switchFan', comet_do_switchFan_handler)
        return g.sijax.process_request()

    return render_template('index.html')

@app.route('/sensors', methods=['POST']) 
def sensors():
    try:
	
        sensors = request.args.get("sensors")
        sensorslist=sensors.split(",")
        r.set('timevalue',sensorslist[0])
        r.set('tempvalue',sensorslist[3])
        r.set('lightvalue',sensorslist[1])
        r.set('moisvalue',sensorslist[2])
        r.set('distancevalue',sensorslist[4])
        print "Time:" + str(sensorslist[0])
        print "Light:" + str(sensorslist[1])
        print "Moisture:" + str(sensorslist[2])
        print "Temperature:" + str(sensorslist[3])
        print "Distance:" + str(sensorslist[4])
		
        if r.get('fanswitch') == "off":
            fan=0
        elif r.get('fanswitch') == "on":
            fan=1
		
        if r.get('ledswitch') == "off":
            led=0
        elif r.get('ledswitch') == "on":
            led=1
		
        waterpump=0
		
        mysql
        conn = mysql.connect()
        cursor = conn.cursor()
    
        sql ="INSERT INTO sensors VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')" % (sensorslist[0],sensorslist[3],sensorslist[1],sensorslist[2],sensorslist[4], str(led),str(fan),str(waterpump))
        print "SQL=" + sql
        numrow=cursor.execute(sql) 
        if numrow > 0:
            conn.commit()
			
	    print "Inserted:" + str(numrow) +" row"
    except Exception as e:
        print "Error:" + str(e)
        return json.dumps({'error':str(e)})
    finally:
        cursor.close()
        conn.close()
        return "sensors:" + str(sensors)

@app.route('/alertsremote', methods=['POST']) 
def alertsremote():
    try:
        r.set('alerttimevalue',aslocaltimestr(datetime.utcnow()))
        r.set('alertdistancevalue','0')
        r.set('alertcam','0')
        filename = request.args.get("filename")
        r.set('alertsnapshotfilename',str(filename))		
        alerts = request.args.get("alerts")        
        r.set('alertmessage',alerts)
        print "Alerts:" + str(alerts)
        
    except Exception as e:
        print "Error:" + str(e)
        return json.dumps({'error':str(e)})
    finally:
        return "sensors"
		
@app.route('/alerts', methods=['POST']) 
def alerts():
    try:
        r.set('alertcam','1')
        filename = request.args.get("filename")	

        sensors = request.args.get("sensors")
        sensorslist=sensors.split(",")
        r.set('alertsnapshotfilename',str(filename))
        r.set('alerttimevalue',sensorslist[0])
        r.set('alertdistancevalue',sensorslist[4])
		
        print "Time:" + str(sensorslist[0])
        print "Distance:" + str(sensorslist[4])
		
        alerts = request.args.get("alerts")
        
        r.set('alertmessage',alerts)

        print "Alerts:" + str(alerts)
        aws=''
        
        mysql
        conn = mysql.connect()
        cursor = conn.cursor()
    
        sql ="INSERT INTO alerts VALUES ('%s','%s','%s','%s','%s')" % (sensorslist[0],filename,sensorslist[4],aws,alerts)
        print "SQL=" + sql
        numrow=cursor.execute(sql) 
        if numrow > 0:
            conn.commit()
			
	    print "Inserted:" + str(numrow) +" row"
    except Exception as e:
        print "Error:" + str(e)
        return json.dumps({'error':str(e)})
    finally:
        cursor.close()
        conn.close()
        return "sensors:" + str(sensors)
    



if __name__ == "__main__":
    r.set('ledswitch',"off")
    r.set('fanswitch',"off")
    r.set('alertsnapshotfilename','')
    r.set('alerttimevalue','')
    r.set('alertdistancevalue','')
    r.set('alertmessage','')
    r.set('alertcam','0')
    app.run(debug=False,host='0.0.0.0', port=int(os.getenv('PORT', '5000')))
    
