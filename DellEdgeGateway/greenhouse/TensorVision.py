import requests
import json

subscription_key = "yytt6688"
assert subscription_key

vision_base_url = "http://172.24.5.157:5000/"
vision_analyze_url = vision_base_url + "analyzeImage"

image_path = "snapshot.jpg"
file_path='/opt/greenhouse/'
def Tvision():
	response=''
	image_data = open(file_path+image_path, 'rb')
	headers    = {'Subscription-Key': subscription_key, 
				  "Content-Type": "application/octet-stream" }
	params     = {'image': image_path}
	files = {'file':image_data}
	try:	
		response = requests.post(vision_analyze_url,files=files)
		if response is not '':
			return response.text.replace('\n','<br>')
		
	finally:
		image_data.close()
		return response
		
		
if __name__ == '__main__':
	resp=Tvision()
	print resp
