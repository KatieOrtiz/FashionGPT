from flask import Flask, request, render_template, redirect, url_for, jsonify, flash, send_from_directory, abort, session
from flask_login import UserMixin, LoginManager, login_required, login_user, logout_user, current_user

import mysql.connector

app = Flask(__name__)

# Set the secret key for the application
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# db connection settings
db_config = {
    'user': 'db_admin',
    'password': 'dbpass',
    'host': '130.166.160.21',
    'database': 'fashion_gpt',
}

login_manager = LoginManager()
login_manager.init_app(app)
# login_manager.login_view = 'login'

app.secret_key = '123'

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

@app.route('/')
def index():
    return render_template('frontPage.html')

@app.route('/frontPage')
def frontPage():
    return render_template('frontPage.html')

@app.route('/emailVerification', methods=['GET', 'POST'])
def emailVerification():
    if request.method == 'POST':
        email = request.form.get('email')

        # Check if the email exists in the Users table
        query = "SELECT * FROM Users WHERE email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()

        if result:
            # Email exists, redirect to homePage or any other appropriate route
            return redirect(url_for('passwordPage'))
        else:
            # Email does not exist, redirect to register page
            return redirect(url_for('register'))

    return render_template('emailVerification.html')

@app.route('/homePage')
def homePage():
    return render_template('homePage.html')

@app.route('/passwordPage', methods=['GET', 'POST'])
def passwordPage():
    if request.method == 'POST':
        password = request.form.get('password')

        # Check if the password exists in the Users table
        query = "SELECT * FROM Users WHERE password = %s"
        cursor.execute(query, (password,))
        result = cursor.fetchone()

        if result:
            # Password exists, redirect to homePage or any other appropriate route
            return redirect(url_for('homePage'))
        else:
            # Password is incorrect, display passwordPage page again with a message that the password is incorrect
            flash('Incorrect password. Please try again.', 'error')
            return redirect(url_for('passwordPage'))
    else:
        # If it's a GET request, render the passwordPage template
        return render_template('passwordPage.html')

@app.route('/userProfile')
def userProfile():
    return render_template('userProfile.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Insert user data into the Users table
        query = "INSERT INTO Users (username, email, password) VALUES (%s, %s, %s)"
        cursor.execute(query, (username, email, password))
        conn.commit()

        # Redirect to the homePage or any other appropriate route
        return redirect(url_for('homePage'))

    return render_template('register.html')

@app.route('/registersize', methods=['GET', 'POST'])
def registersize():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        neck = request.form.get('neck')
        chest = request.form.get('chest')
        sleeve = request.form.get('sleeve')

        # Insert user data into the Users table
        user_query = "INSERT INTO Users (username, email, password) VALUES (%s, %s, %s)"
        cursor.execute(user_query, (username, email, password))
        conn.commit()

        # Retrieve user_id of the newly inserted user
        user_id = cursor.lastrowid

        # Insert size measurements into the Measurements table
        size_query = "INSERT INTO Measurements (user_id, neck, chest, sleeve) VALUES (%s, %s, %s, %s)"
        cursor.execute(size_query, (user_id, neck, chest, sleeve))
        conn.commit()

        # Redirect to the homePage or any other appropriate route
        return redirect(url_for('homePage'))

    return render_template('registersize.html')


@app.route('/registersize2', methods=['GET', 'POST'])
def registersizetwo():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        waist = request.form.get('pWaist')
        inseam = request.form.get('inseam')
        hip = request.form.get('hip')

        # Insert user data into the Users table
        user_query = "INSERT INTO Users (username, email, password) VALUES (%s, %s, %s)"
        cursor.execute(user_query, (username, email, password))
        conn.commit()

        # Retrieve user_id of the newly inserted user
        user_id = cursor.lastrowid

        # Insert pant size measurements into the PantMeasurements table
        size_query = "INSERT INTO PantMeasurements (user_id, waist, inseam, hip) VALUES (%s, %s, %s, %s)"
        cursor.execute(size_query, (user_id, waist, inseam, hip))
        conn.commit()

        # Redirect to the homePage or any other appropriate route
        return redirect(url_for('homePage'))

    return render_template('registersize2.html')


@app.route('/sizePreference')
def sizePreference():
    return render_template('sizePreference.html')

@app.route('/changePassword')
def changePassword():
    return render_template('changePassword.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)