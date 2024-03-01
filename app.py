from flask import Flask, request, render_template, redirect, url_for, session, flash
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

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

        flash('User registered successfully!')
        return redirect(url_for('login'))
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
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid password. Try again.')
    return render_template('verify_password.html')

@app.route('/dashboard')
@login_required
def home():
    return render_template('dashboard.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
