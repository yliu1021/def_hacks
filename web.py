from flask import Flask, render_template, request, flash, redirect
from werkzeug import secure_filename
app = Flask(__name__)

@app.route('/' , methods = ['GET','POST'])
def home():
	if request.method == 'POST':
		f = request.files['file']
		f.save(secure_filename(f.filename))
	return render_template('index.html')
   
if __name__ == '__main__':
   app.run(debug = True)