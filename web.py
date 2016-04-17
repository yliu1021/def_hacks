from flask import Flask, render_template, request, flash, redirect
from werkzeug import secure_filename
import os

UPLOAD_FOLDER = 'static'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/' , methods = ['GET','POST'])
def home():
	if request.method == 'POST':
		f = request.files['file']
		filename = secure_filename(f.filename)
		print(filename)
		f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	return render_template('index.html')
   
if __name__ == '__main__':
   app.run(debug = True)