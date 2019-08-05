#!/usr/bin/env python

import os
from flask import Flask, abort, request 
import classify_image
import sendMail

app_path='/opt/models/tutorials/image/imagenet/'
app = Flask(__name__)

file_name='snapshot.jpg'

@app.route('/analyzeImage', methods=['POST']) 
def analyzeImage():
    result=''
    body_text=''
    try:
        imagefile = request.files['file']
        if imagefile:
            #print 'image file='
            #print imagefile
            imagefile.save(app_path+file_name)
            result=classify_image.analyzeImage(file_name)
            #print 'result:'
            #print result
			
            emails = ["user1@sgcloud.com"]
            #cc_emails = ["someone@gmail.com"]
            #bcc_emails = ["anonymous@circe.org"]
 
            subject = "Intruder near the Greenhouse!"
            body_text = "According to TensorFlow Image analysis, it could be: \n"
            res = result.split(';')
            for r in res:
                body_text = body_text + r + '\n'
            path = app_path+file_name
            sendMail.send_email_with_attachment(subject, body_text, emails,"", "", path)
    except Exception as e:
        print e
    finally:
        return body_text
	



if __name__ == "__main__":
	app.run(debug=False,host='0.0.0.0', port=int(os.getenv('PORT', '5000')))