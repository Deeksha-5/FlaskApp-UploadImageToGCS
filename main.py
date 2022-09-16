from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
import os
import google.cloud.storage as storage
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


app.config['UPLOAD_CONFIG'] = '/tmp'
@app.route('/upload')
def upload_file():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload():
   if request.method == 'POST':
      f = request.files['file']
      full_file_path = os.path.join(app.config['UPLOAD_CONFIG'],secure_filename(f.filename)) 
      f.save(os.path.join(full_file_path))
      client = storage.Client(project='MY_PROJECT-ID')
      bucket = client.get_bucket('MY_BUCKET')
      blob = bucket.blob('file1.jpg')
      with open(full_file_path,'rb') as file:
        blob.upload_from_file(file)
      filename = 'http://upload-dot-MY_PROJECT_ID.appspot.com/uploads/' + full_file_path.split('/')[-1]
      return render_template('uploaded.html',filename=filename)
   else:
      return 'method not allowed'
@app.route('/uploads/<filename>')
def send_file(filename):
    logging.info(filename)
    return send_from_directory(app.config['UPLOAD_CONFIG'], filename)

@app.route('/readiness_check', methods=['GET'])
def readiness_check():
  return '', 200
		
if __name__ == '__main__':
   app.run(debug = True)
