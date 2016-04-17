from flask import Flask, render_template, request, flash, redirect, make_response
from werkzeug import secure_filename
import os
import ImageRecognition

import json

UPLOAD_FOLDER = 'static/'
ALLOWED_EXTENSIONS = ['jpg', 'png', 'jpeg', 'gif']

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    
@app.route('/' , methods = ['GET','POST'])
def home():
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        f.save(filepath)
        
        r = ImageRecognition.getResponse(filepath,
            ImageRecognition.labelFeature,
            ImageRecognition.textFeature,
            ImageRecognition.faceFeature,
            ImageRecognition.landmarkFeature,
            ImageRecognition.logoFeature
            )
        response = make_response(json.dumps(r), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        return render_template('index.html')

if __name__ == '__main__':
   app.run(debug = True)