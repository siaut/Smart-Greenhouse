from flask import Flask, render_template_string
from flask_s3 import FlaskS3, create_all

app = Flask(__name__)
app.config['S3_BUCKET_NAME'] = 'iotcamera01'
app.config['USE_S3_DEBUG'] = True

s3 = FlaskS3(app)

@app.route('/')
def index():
    template_str = """{{ url_for('static', filename="foo.js") }}"""
    return render_template_string(template_str)

def upload_all():
    create_all(app, user='AKIAIBQRFECMKQKXSPFQ', password='KfiSwIjBXfzcyrTomlstr/N0U/Q8Nl/osoflBzUc')

if __name__ == '__main__':
    app.run(debug=True)