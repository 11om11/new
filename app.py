
import os
from flask import Flask, flash, request, redirect, url_for,render_template,send_from_directory,session,g
from werkzeug.utils import secure_filename
import json
UPLOAD_FOLDER = 'E://web development//static'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] =UPLOAD_FOLDER
with open('config.json','r')as c:
    params = json.load(c)["params"]


@app.route('/Homepage')
def Homepage():
   ## if g.user:
        return render_template('homepage.html',user=session['user'])
   
@app.route('/',methods=['GET' , 'POST'])
def login():

    if request.method  == 'POST':
        session.pop('user',None)

        if request.form['password'] =="password":
            session['user'] = request.form['username']
            return redirect(url_for('Homepage'))
    return render_template('Login.html')   

@app.before_request
def before_request():
    g.user = None     

    if 'user' in session:
        g.user = session['user']   

@app.route('/download')
def download():
    return render_template('load.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload_file', name=filename))
    return render_template('upload.html')

DOWNLOAD_DIRECTORY = "notes-sharing-flask\\static"
@app.route('/get-files/<path:path>',methods = ['GET','POST'])
def get_files(path):

    """Download a file."""
    try:
        return send_from_directory(DOWNLOAD_DIRECTORY, path, as_attachment=True)
    except FileNotFoundError:
        os.abort(404)


if  __name__ =="__main__":
    app.run(debug=True)
