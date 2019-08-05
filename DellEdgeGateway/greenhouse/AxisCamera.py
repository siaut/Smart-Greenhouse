import time
import datetime
import requests
from requests.auth import HTTPDigestAuth
import boto
from boto.s3.connection import S3Connection 
import os 
from SimpleCV import Camera

width = 640
height = 480
 

ecs_access_key_id = 'user1'  
ecs_secret_key = 'cfgIT4b11yiumMgny0ygGtMIjv7OvSVaYfcZaKU2'

aws_access_key_id = 'AKIAIBQRFECMKQKXSPFQ'  
aws_secret_key = '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'

ECS_HOST='ecs-lb.sgcloud.com'
ECS_PORT=9020

file_name='snapshot.jpg'
file_path='/opt/greenhouse/'
bname = 'iotcamera01'
AXIS_CAMERA_URL='http://172.24.4.71/jpg/image.jpg?size=3'

def uploadToAWS(filename=file_name):
	#### This is the AWS S3 syntax
	session = boto.connect_s3(aws_access_key_id, aws_secret_key)

	#### Get bucket and display details
	b = session.get_bucket(bname)
	print "S3 connection is: " + str(session)
	print "Bucket is: " + str(b)

	#### Create new key, define metadata, upload and ACL
	k = b.new_key(filename)
	k.set_metadata('webcam', 'yes')
	k.set_contents_from_filename(file_path+file_name)
	k.set_acl('public-read')

	print "Snapshot uploaded to AWS S3."

def uploadToECS():

	session = S3Connection(aws_access_key_id= ecs_access_key_id,  
						aws_secret_access_key= ecs_secret_key,  
						host=ECS_HOST,  
						port=ECS_PORT,  
						calling_format='boto.s3.connection.ProtocolIndependentOrdinaryCallingFormat',  
						is_secure=False)  

	#### This is the ECS syntax. It requires "host" parameter
	#session = boto.connect_s3(ecs_access_key_id, ecs_secret_key, host='ecs1.sgcloud.com')

	#### Get bucket and display details
	b = session.get_bucket(bname)
	print "S3 connection is: " + str(session)
	print "Bucket is: " + str(b)

	currenttime=datetime.datetime.now().strftime('%Y-%m-%dT%H-%M-%S')
	print "time:" + currenttime

	#### Create new key, define metadata, upload and ACL
	k = b.new_key(str(currenttime)+"-"+ file_name)
	k.set_metadata('webcam', 'yes')
	k.set_contents_from_filename(file_path+file_name)
	k.set_acl('public-read')

	print "Snapshot uploaded to ECS."
	return str(currenttime)+"-"+ file_name

def takesnapshotUSB():
	#os.system('fswebcam -r 320x240 -S 3 --jpeg 50 --save /home/pi/to_transmit/%H%M%S.jpg') # uses Fswebcam to take picture
	#os.system('fswebcam -r 640x480 --no-banner --save ' + file_path + file_name) # uses Fswebcam to take picture
	cam = Camera()
	time.sleep(0.1)  # If you don't wait, the image will be dark
	img = cam.getImage()
	img.save(file_path + file_name)

def takesnapshot():
    with open(file_name, 'wb') as handle:
            image_url=AXIS_CAMERA_URL
            response = requests.get(image_url, auth=HTTPDigestAuth('root', 'pass'))

            if not response.ok:
                print response

            for block in response.iter_content(1024):
                if not block:
                    break

                handle.write(block)
                print "Snapshot saved."

if __name__ == '__main__':
	#takesnapshot()
	#uploadToECS()
	takesnapshotUSB()
	#uploadToAWS()

