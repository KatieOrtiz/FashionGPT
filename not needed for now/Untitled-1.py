
# a) Routes.py
#
# b) 3/12/23 - Present
#
# c) Grant Freedman
#    Charitha W.
#    Robert K.
#    Shelby Gallegos
#
# d) This class handles the webpage routes for our user interactivity and directs users to specific pages
#    depending on their actions. Routes also can gets user entered data from the webpage using  
# e) IMPORTANT FUNCTIONS:
#        upload()    : utilizes dropzone to import and store file through our webpage application
#        send()      : accepts and stores uploaded file parameters to correctly send and store files
#        dashboard() : the homepage for our web application and acts as the main terminal for all our branching functions
#
# f) utilizes imported data structures from other files (files <- send.py, users <- quickclip.py)
#   
# g) NONE

#=======================IMPORTS===================
from flask import Flask, request, render_template, redirect, url_for, jsonify, flash, send_from_directory, abort, session
from flask_login import UserMixin, LoginManager, login_required, login_user, logout_user, current_user
from quickclip import users, create_user, User, login, register, generate_key, key_match
from send import send_file, upload_file, files
from recieve import recieve_file, SERVER_PORT
import socket
import zipfile
import shutil
import os
from flask_dropzone import Dropzone
import argparse
#================END OF IMPORTS===================


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config.update(
    UPLOADED_PATH=os.path.join(basedir, 'send'),
    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_CUSTOM = True,
    DROPZONE_ALLOWED_FILE_TYPE='image/*, audio/*, video/*, text/*, app/*, .docx, .pdf, .jar, .zip, .app',
    DROPZONE_MAX_FILE_SIZE=80,
    DROPZONE_MAX_FILES=100,
)

dropzone = Dropzone(app)

login_manager = LoginManager()
login_manager.init_app(app)

app.secret_key = '123'

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

@app.route('/upload', methods=['POST', 'GET'])
def upload():

    """
    upload(): uses the upload.html to create a drag and drop area that allows a user to upload
    their file into the app directory. This gives us the capability to acces data and parameters
    to ultimately send.
    """
    if request.method == 'POST':
        f = request.files.get('file')
        username = session.get('username')
        subfolder_path = os.path.join(app.config['UPLOADED_PATH'], username)
        os.makedirs(subfolder_path, exist_ok=True)
        file_path = os.path.join(subfolder_path, f.filename)
        f.save(file_path)
        upload_file(file_path)

    return render_template('upload.html')


@app.route('/login', methods=['GET', 'POST'])
def login_route():
    return login()


@app.route('/register', methods=['GET', 'POST'])
def register_route():
    
    return register()


@app.route('/gen_key', methods=['GET'])
def gen_key():
    return jsonify(generate_key())


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/send')
def send():
    global SERVER_PORT
    username = session.get('username')
    subfolder_path = os.path.join(app.config['UPLOADED_PATH'], username)
    subfolder_path_transfer = os.path.join(app.config['UPLOADED_PATH'], username) + ".zip"

    output_path = os.path.join( "send", f"{username}.zip")
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zip_obj:
        for filename in os.listdir(subfolder_path):
            file_path = os.path.join(subfolder_path, filename)
            if os.path.isfile(file_path):
                zip_obj.write(file_path, arcname=filename)

    host = '127.0.0.1'
    print(subfolder_path_transfer, host, SERVER_PORT)
    send_file(subfolder_path_transfer, host, SERVER_PORT)
    SERVER_PORT += 1
    print(f"send port AFTER: {SERVER_PORT}")
    os.remove(subfolder_path_transfer)
    shutil.rmtree(subfolder_path)
        
    return redirect(url_for('index'))


@app.route('/recieve')
def receive():
    recieve_file()
    return render_template("index.html")

@app.route('/')
def index():
    
    return render_template("index.html")


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/key_match', methods=['POST'])
def matching():
    key_matches = key_match(request.form['key'])
    if key_matches :
        return render_template('upload.html')
    else:
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        else:
            flash('INVALID CODE!')
            return redirect(url_for('index'))

# app.config["CLIENT_FILES"] = "/routes/recieve/"
# @app.route('/download', methods=['GET', 'POST'])
# def download():
#     try:
#         filename = session.get('username') + ".zip"
#         return send_from_directory(app.config["CLIENT_FILES"], filename, as_attachment=True)
#     except FileNotFoundError:
#         abort(404);