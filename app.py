from flask import Flask, render_template, request
from google.cloud import storage

app = Flask(__name__)

storage_client = storage.Client()
bucket = storage_client.bucket('nadella-files')

import google.auth

creds, project = google.auth.default()
print(f"Using credentials from: {creds}")

@app.route("/test-upload")
def test_upload():
    bucket = storage_client.bucket("nadella-files")
    blob = bucket.blob("test_upload.txt")
    blob.upload_from_string("Hello from Flask!")
    return "Uploaded!"

@app.route('/')
def index():
    return render_template('index.html')  # Render file index.html

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    blob = bucket.blob(file.filename)
    blob.upload_from_file(file)
    return f'File {file.filename} uploaded to {bucket.name}.'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
