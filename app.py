from flask import Flask, render_template, request, redirect, url_for, flash
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
    return render_template('passwordPage.html')

@app.route('/personalDetails')
def personalDetails():
    return render_template('personalDetails.html')

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

@app.route('/sizePreference')
def sizePreference():
    return render_template('sizePreference.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)