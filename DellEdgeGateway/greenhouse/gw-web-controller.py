#!/usr/bin/env python

import os
from flask import Flask, abort, request, redirect
import AxisCamera
import TensorVision
import vision
import requests


app = Flask(__name__)
app_path='/opt/greenhouse/'
file_name='cloudswitch.txt'
image_fname='snapshot.jpg'

API_ENDPOINT_ALERT = "http://gh-controller.apps.csc-dell.com/alertsremote"

def check_cloudswitch():
	cloudswitch="off"
	try:
		file = open(app_path+file_name,'r')
		cloudswitch= file.read()
		print "cloudswitch=" + cloudswitch
	finally:
		file.close()
		
	return cloudswitch
	
@app.route('/cloud', methods=['POST']) 
def cloud():
	cloudswitch = check_cloudswitch()
	switch = request.args.get("switch")
	try:	
		file = open(app_path+file_name,'w') 
		if switch == "on":
			file.write("on")
			print '...cloud on'
		else:
			file.write("off")
			print '...cloud off'
	finally:
		file.close()
		
	return switch

@app.route('/remote', methods=['POST']) 
def remote():

    try:
        imagefile = request.files['file']
        if imagefile:
            imagefile.save(app_path+image_fname)
			
            filename=AxisCamera.uploadToECS()
            print "filename:"+filename
            cloudswitch=check_cloudswitch()
            if cloudswitch=="on":
				AxisCamera.uploadToAWS(filename)
				vresp = vision.MSvision()
            else:
				vresp = TensorVision.Tvision()
			
            print vresp
            PARAMS_ALERT = {'filename':filename,'alerts':vresp} 
            r2 = requests.post(url = API_ENDPOINT_ALERT, params = PARAMS_ALERT, verify=False)
		
    except Exception as e:
        print(e)
		
    finally:
        return redirect("http://greenhouse.apps.csc-dell.com", code=302)

if __name__ == "__main__":
	app.run(debug=False,host='0.0.0.0', port=int(os.getenv('PORT', '5000')))