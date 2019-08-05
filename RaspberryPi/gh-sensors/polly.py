import boto3
import subprocess
import os
import time

aws_access_key_id = 'AKIAISQ3GX66CAWEC3VQ'
aws_secret_access_key = '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'
region_name='ap-southeast-1'

talk_to_me = "<speak>Please keep a distance from the plants.<break time=\"1s\"/></speak> "

def recordPolly(voiceid, filename):
	polly = boto3.client('polly', region_name=region_name)

	response = polly.synthesize_speech(
		OutputFormat='mp3',
		Text=talk_to_me,
		TextType='ssml',
		VoiceId=voiceid)
		
		#Joanna
		#Mizuki

	with open(filename, 'wb') as f:
		f.write(response['AudioStream'].read())

def speakfromRecording(filename):
	subprocess.call(["/usr/bin/omxplayer",filename])

def initVoice():
	recordPolly('Joanna','english.mp3')
	recordPolly('Mizuki','japanese.mp3')
	
def speakBoth():
	speakfromRecording('english.mp3')
	speakfromRecording('japanese.mp3')

if __name__ == '__main__':
	initVoice()
	
	



