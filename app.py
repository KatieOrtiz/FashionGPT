from flask import request, render_template, redirect, url_for, session, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta, timezone
from flask_cors import CORS
from models import User, UserQuery
import jwt
from extensions import app, db, login_manager

from haiku import one_getUserData

CORS(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(email=email).first():
            flash('Email already exists.')
            return redirect(url_for('register'))

        new_user = User(username=username, email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        token = jwt.encode({'user': email, 'exp': datetime.now(timezone.utc) + timedelta(hours=12)}, app.secret_key)
        flash('User registered successfully!')
        resp = redirect(url_for('dashboard'))
        resp.set_cookie('x-access-token', token)
        return resp
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        if not email:
            flash('Please enter an email address.')
            return render_template('login.html')

        # Check if the email exists in the database
        user = User.query.filter_by(email=email).first()
        if user is None:
            flash('No account found with that email address.')
            return render_template('login.html')
        # If user exists, proceed to verify password
        session['email'] = email
        return redirect(url_for('verify_password'))

    return render_template('login.html')

@app.route('/verify_password', methods=['GET', 'POST'])
def verify_password():
    if 'email' not in session:
        return redirect(url_for('login'))
    email = session['email']
    user = User.query.filter_by(email=email).first()
    if request.method == 'POST':
        if user and user.check_password(request.form['password']):
            login_user(user)
            token = jwt.encode({'user': email, 'exp': datetime.now(timezone.utc) + timedelta(hours=12)}, app.secret_key)
            resp = redirect(url_for('dashboard'))
            resp.set_cookie('x-access-token', token)
            return resp
        else:
            flash('Invalid password. Try again.')
    return render_template('verify_password.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/pref', methods=['GET', 'POST'])
@login_required
def pref():
    if request.method == 'POST':
        gender = request.form['gender']
        weight = request.form['weight']
        waist = request.form['waist']
        length = request.form['length']
        Skintone = request.form['Skintone']
        height = request.form['height']
        hair = request.form['hair']
        build = request.form['build']
        Budget = request.form['Budget']
        Colors = request.form['Colors']
        age = request.form['age']
        Style = request.form['Style']
        Season = request.form['Season']
        fabric = request.form['fabric']
        usersRequest = request.form['usersRequest']
        
        #logging to DB
        email = session['email']
        user = User.query.filter_by(email=email).first()
        user_id = user.id
        query = UserQuery(user_id=user_id , gender=gender, weight=weight, waist=waist, length=length, Skintone=Skintone, height=height, hair=hair, build=build, Budget=Budget, Colors=Colors, age=age, Style=Style, Season=Season, fabric=fabric, usersRequest=usersRequest)
        db.session.add(query)
        db.session.commit()
        generated_id = query.id
        print(f'The generated ID for the newly inserted row is: {generated_id}')

        #sending query to AI
        one_getUserData(generated_id=generated_id, gender=gender, weight=weight, waist=waist, length=length, Skintone=Skintone, height=height, hair=hair, build=build, Budget=Budget, Colors=Colors, age=age, Style=Style, Season=Season, fabric=fabric, usersRequest=usersRequest)
        
        resp = redirect(url_for('dashboard'))
        return resp
    return render_template('reigstersize.html')


# @app.route('/registersize', methods=['GET', 'POST'])
# def registersize():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         email = request.form.get('email')
#         password = request.form.get('password')
#         neck = request.form.get('neck')
#         chest = request.form.get('chest')
#         sleeve = request.form.get('sleeve')

#         # Insert user data into the Users table
#         user_query = "INSERT INTO Users (username, email, password) VALUES (%s, %s, %s)"
#         cursor.execute(user_query, (username, email, password))
#         conn.commit()

#         # Retrieve user_id of the newly inserted user
#         user_id = cursor.lastrowid

#         # Insert size measurements into the Measurements table
#         size_query = "INSERT INTO Measurements (user_id, neck, chest, sleeve) VALUES (%s, %s, %s, %s)"
#         cursor.execute(size_query, (user_id, neck, chest, sleeve))
#         conn.commit()

#         # Redirect to the homePage or any other appropriate route
#         return redirect(url_for('homePage'))

#     return render_template('registersize.html')


# @app.route('/registersize2', methods=['GET', 'POST'])
# def registersizetwo():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         email = request.form.get('email')
#         password = request.form.get('password')
#         waist = request.form.get('pWaist')
#         inseam = request.form.get('inseam')
#         hip = request.form.get('hip')

#         # Insert user data into the Users table
#         user_query = "INSERT INTO Users (username, email, password) VALUES (%s, %s, %s)"
#         cursor.execute(user_query, (username, email, password))
#         conn.commit()

#         # Retrieve user_id of the newly inserted user
#         user_id = cursor.lastrowid

#         # Insert pant size measurements into the PantMeasurements table
#         size_query = "INSERT INTO PantMeasurements (user_id, waist, inseam, hip) VALUES (%s, %s, %s, %s)"
#         cursor.execute(size_query, (user_id, waist, inseam, hip))
#         conn.commit()

#         # Redirect to the homePage or any other appropriate route
#         return redirect(url_for('homePage'))

#     return render_template('registersize2.html')


# @app.route('/sizePreference')
# def sizePreference():
#     return render_template('sizePreference.html')

# @app.route('/changePassword')
# def changePassword():
#     return render_template('changePassword.html')



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
