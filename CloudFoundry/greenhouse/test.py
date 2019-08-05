#!/usr/bin/env python
import datetime

import pytz
from time import time

utc_now = pytz.utc.localize(datetime.datetime.utcnow())
epoch = datetime.datetime(1970,1,1, tzinfo=pytz.utc)

pst_now = utc_now.astimezone(pytz.timezone("Asia/Singapore"))
epoch2 = datetime.datetime(1970,1,1, tzinfo=pytz.timezone("Asia/Singapore"))
ts = (pst_now -epoch2).total_seconds()


us = (utc_now - epoch).total_seconds()

print time()
print utc_now
print us
print "SG:" + str(pst_now)
print ts


from time import time
import json
import urllib
from urlparse import urlparse
import httplib2 as http #External library


strtime="2018-02-24T22:47:00"
#apiurl='https://api.data.gov.sg/v1/environment/air-temperature?date_time'+strtime
#apiurl=urlparse(apiurl)

#f = urllib2.urlopen(apiurl)
#json_string = f.read()
#parsed_json = json.loads(json_string)
#print parsed_json
#location = parsed_json['location']['city']
#temp_f = parsed_json['current_observation']['temp_f']
#print "Current temperature in %s is: %s" % (location, temp_f)
#f.close()

#Authentication parameters
headers = { 'AccountKey' : '6HsAmP1e0R/EkEYWOcjKg==','accept' : 'application/json'} #this is by default
#API parameters
uri = 'https://api.data.gov.sg' #Resource URL
path = '/v1/environment/air-temperature?date_time='+strtime
#Build query string & specify type of API call
target = urlparse(uri + path)
print target.geturl()
method = 'GET'
body = ''
#Get handle to http
h = http.Http()
#Obtain results
response, content = h.request(
target.geturl(),
method,
body,
headers)
#Parse JSON to print
jsonObj = json.loads(content)
id=11
print jsonObj['metadata']['stations'][id]
print jsonObj['metadata']['stations'][id]['name']
print ""
print jsonObj['items'][0]['readings'][id]
print ""
print jsonObj['items'][0]['readings'][id]['value']


#print json.dumps(jsonObj, sort_keys=True, indent=4)
#Save result to file
#with open("traffic_incidents.json","w") as outfile: #Saving jsonObj["d"]
#json.dump(jsonObj, outfile, sort_keys=True, indent=4, ensure_ascii=False)

print time()*1000
