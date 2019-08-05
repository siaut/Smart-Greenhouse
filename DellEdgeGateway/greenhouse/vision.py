import requests
import json

#subscription_key = "f86887ce0f904a0694425aeec909269b"
subscription_key = "9a7373fef0a148c798723cb3fa2c4152"
assert subscription_key

#vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v1.0/"
vision_base_url = "https://westus.api.cognitive.microsoft.com/vision/v1.0/"

vision_analyze_url = vision_base_url + "analyze"

image_path = "snapshot.jpg"

def MSvision():
	image_data = open(image_path, "rb").read()
	headers    = {'Ocp-Apim-Subscription-Key': subscription_key, 
				  "Content-Type": "application/octet-stream" }
	params     = {'visualFeatures': 'Categories,Description,Color'}
	response   = requests.post(vision_analyze_url, 
							   headers=headers, 
							   params=params, 
							   data=image_data)

	response.raise_for_status()

	analysis      = response.json()
	image_caption = analysis["description"]["captions"][0]["text"].capitalize()
	image_caption_percent=analysis["description"]["captions"][0]["confidence"]
	result="{} {:0.2f}%".format(image_caption, image_caption_percent*100)
	result = "According to Azure Vision Analysis, it could be:;" + result
	print result
	result = result + ";Categories:"
	print("\nCategories:")
	for tag in analysis["categories"]:
		image_category = tag["name"]
		image_category_percent = tag["score"]
		result = result + ";{} {:0.2f}%".format(image_category, image_category_percent*100)
		print("{} {:0.2f}%".format(image_category, image_category_percent*100))

	result = result + ";Tags:"
	print("\nTags:")
	for tags in analysis["description"]["tags"]:
		image_tags = tags
		result = result + ";{}".format(image_tags)
		print("{}".format(image_tags))
	
	return result
		
	#print json.dumps(analysis, indent=4, sort_keys=True)
if __name__ == '__main__':
	resp=MSvision()
	print resp
