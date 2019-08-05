import urllib2
import json

f = urllib2.urlopen('http://api.wunderground.com/api/569f4057fcdc5f4c/geolookup/conditions/q/Singapore/Singapore.json')
json_string = f.read()
parsed_json = json.loads(json_string)
location = parsed_json['location']['city']
temp_f = parsed_json['current_observation']['temp_c']
print json.dumps(parsed_json, sort_keys=True, indent=4)
print "Current temperature in %s is: %s" % (location, temp_f)
UV = parsed_json['current_observation']['UV']
print "UV:" + UV
icon= parsed_json['current_observation']['icon']
print icon
icon_url= parsed_json['current_observation']['icon_url']
print icon_url
relative_humidity= parsed_json['current_observation']['relative_humidity']
print "Relative Humidity:" + relative_humidity

f.close()

#http://api.wunderground.com/api/569f4057fcdc5f4c/conditions/q/CA/San_Francisco.json