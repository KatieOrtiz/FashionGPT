from flask import Flask, request, render_template, redirect, url_for, session, flash, jsonify
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
# from dotenv import load_dotenv
import jwt
import datetime
from functools import wraps
#importing from python_scripts folder
# from python_scripts import scraper

import os
import mysql.connector


# Load environment variables from .env file
# def configure():
#     load_dotenv()

#call configure function to load environment variables
# configure()
#call os.getenv(API_KEY) to get the API_KEY value

app = Flask(__name__)
app.secret_key = '123'

# Database connection settings
db_config = {
    'user': 'db_admin',
    'password': 'dbpass',
    'host': '130.166.160.21',
    'database': 'fashion_gpt',
}



# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User class for Flask-Login
class User(UserMixin):
    def __init__(self, user_id, username, email):
        self.id = user_id
        self.username = username
        self.email = email


#validating user JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401
        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated


# Flask-Login user loader
@login_manager.user_loader
def load_user(user_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM Users WHERE user_id = %s', (user_id,))
    user_record = cursor.fetchone()
    cursor.close()
    conn.close()
    if user_record:
        return User(user_id=user_record['user_id'], username=user_record['username'], email=user_record['email'])
    return None

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Users (username, email, password) VALUES (%s, %s, %s)', (username, email, password))
        conn.commit()
        cursor.close()
        conn.close()
        token = jwt.encode({'user': email, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(hours=12)}, app.secret_key)
        flash('User registered successfully!')
        resp = redirect(url_for('login'))
        resp.set_cookie('x-access-token', token)
        return resp
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['email'] = request.form['email']  # Store email in session for password verification
        return redirect(url_for('verify_password'))
    return render_template('login.html')

@app.route('/verify_password', methods=['GET', 'POST'])
def verify_password():
    if request.method == 'POST':
        email = session.get('email')
        password = request.form['password']

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM Users WHERE email = %s', (email,))
        user_record = cursor.fetchone()
        cursor.close()
        conn.close()

        if user_record and check_password_hash(user_record['password'], password):
            user = User(user_id=user_record['user_id'], username=user_record['username'], email=user_record['email'])
            login_user(user)
            token = jwt.encode({'user': email, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(hours=12)}, app.secret_key)
            resp = redirect(url_for('dashboard'))
            resp.set_cookie('x-access-token', token)
            return resp
        else:
            flash('Invalid password. Try again.')
    return render_template('verify_password.html')

@app.route('/dashboard')
@token_required
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
@token_required
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
