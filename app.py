from operator import or_
from flask import request, render_template, redirect, url_for, session, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta, timezone
from flask_cors import CORS
from models import Suggestion, User, UserQuery, Product
import jwt, os
from extensions import app, db, login_manager
from haiku import one_getUserData

CORS(app)

# Function for login session
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# Function for index page
@app.route('/')
def index():
    return render_template('index.html')

# Function for registering users
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Get user information from form
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Check is user email exists in DB
        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'error')
            return redirect(url_for('register'))

        # Add new user to DB
        new_user = User(username=username, email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

       # token = jwt.encode({'user': email, 'exp': datetime.now(timezone.utc) + timedelta(hours=12)}, app.secret_key)
        flash('User registered successfully!')
        session['email'] = email
        resp = redirect(url_for('pref'))
       # resp.set_cookie('x-access-token', token)
       
       # Check if the favorite_suggestions.txt file exists
        if os.path.exists('favorite_suggestions.txt'):
            # If the favorite_suggestions.txt file exists, delete it
            os.remove('favorite_suggestions.txt')

        # Create the favorite_suggestions.txt file
        with open('favorite_suggestions.txt', 'w'):
            pass
            
        return redirect(url_for('pref'))
    return render_template('register.html')

# Function for logging in a user
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Get email from form
    if request.method == 'POST':
        email = request.form.get('email')
        
        # If the entered value is not in email format, return an error
        if not email:
            flash('Please enter an email address', 'error')
            return render_template('login.html')

        # Check if the email exists in the database
        user = User.query.filter_by(email=email).first()
        if user is None:
            flash('No account found with that email address', 'error')
            return render_template('register.html')
        # Create session with the entered email
        session['email'] = email

        return redirect(url_for('verifyPassword'))

    return render_template('login.html')

# Function to verify user's password
@app.route('/verifyPassword', methods=['GET', 'POST'])
def verifyPassword():
    # Checks if a session currently exists
    if 'email' not in session:
        return redirect(url_for('login'))
    email = session['email']
    user = User.query.filter_by(email=email).first()
    
    # Gets the password from login form and checks against DB if it's the correct password
    if request.method == 'POST':
        if user and user.check_password(request.form['password']):
            login_user(user)
           # token = jwt.encode({'user': email, 'exp': datetime.now(timezone.utc) + timedelta(hours=12)}, app.secret_key)
           
            # Check if the favorite_suggestions.txt file exists
            if os.path.exists('favorite_suggestions.txt'):
                # If the favorite_suggestions.txt file exists, delete it
                os.remove('favorite_suggestions.txt')

            # Create the favorite_suggestions.txt file
            with open('favorite_suggestions.txt', 'w'):
                pass
            
            resp = redirect(url_for('dashboard'))
            #resp.set_cookie('x-access-token', token)
            return resp
        else:
            flash('Invalid password. Try again.', 'error')
    return render_template('verifyPassword.html')

# Function to display the dashboard, including user outfit suggestions
@app.route('/dashboard')
#@login_required
def dashboard():
    
    # Retrieves the user ID via their email in the session
    email = session['email']
    user = User.query.filter_by(email=email).first()

    user_id = user.id
    
    # Retrieve user suggestions from the database and sort by timestamp descending
    user_suggestions = Suggestion.query.filter_by(user_id=user_id).order_by(Suggestion.timestamp.desc()).all()

    # Initialize a dictionary to store product suggestions grouped by user suggestion
    suggestion_products = {}

    # Iterate through user suggestions
    for suggestion in user_suggestions:
        # Initialize list to store products for this suggestion
        suggestion_products[suggestion.id] = []

        # Match product names for each category
        categories = ['top', 'outerwear', 'hat', 'bottoms', 'socks', 'footwear', 'belt']
        for category in categories:
            product_info = getattr(suggestion, category)  # Get product info from suggestion
            
            if product_info:
                # Parse the string to extract the product name
                product_name = product_info.split(',')[0].strip("[]").strip('"').strip("'")
                
                # Query the product table for the matching product
                product = Product.query.filter_by(name=product_name).first()
                if product:
                    suggestion_products[suggestion.id].append({
                        'name': product.name,
                        'price': product.price,
                        'color': product.color,
                        'image': product.image,  
                        'link': product.link,
                    })
                else:
                    # Skip if product doesn't exist
                    pass

    return render_template('dashboard.html', suggestion_products=suggestion_products)

# Function to mark an outfit suggestion as a favorite
@app.route('/mark-favorite', methods=['POST'])
def mark_favorite():
    suggestion_id = request.json['suggestion_id']

    # Read in favorited suggestions from file
    with open('favorite_suggestions.txt', 'r') as f:
        existing_suggestion_ids = [int(line.strip()) for line in f]

    # Check if the suggestion ID already exists
    if suggestion_id in existing_suggestion_ids:
        # Remove the existing suggestion ID from the list
        existing_suggestion_ids.remove(suggestion_id)

        # Write the updated list of suggestion IDs back to the file
        with open('favorite_suggestions.txt', 'w') as f:
            for id in existing_suggestion_ids:
                f.write(str(id) + '\n')
    else:
        # If the suggestion ID does not exist, append it to the file
        with open('favorite_suggestions.txt', 'a') as f:
            f.write(str(suggestion_id) + '\n')

    return 'OK', 200

# Function to check if the outfit suggestion ID is currently marked as favorite
@app.route('/check-favorite')
def check_favorite():
    suggestion_id = request.args.get('suggestion_id')

    with open('favorite_suggestions.txt', 'r') as f:
        favorite_suggestions = f.read().splitlines()
        
    is_favorite = suggestion_id in favorite_suggestions
    return jsonify({'isFavorite': is_favorite})

# Function to remove a favorited outfit suggestion
@app.route('/remove-favorite', methods=['POST'])
def remove_favorite():
    suggestion_id = request.json['suggestion_id']

    with open('favorite_suggestions.txt', 'r') as f:
        favorite_suggestions = f.read().splitlines()
    
    if suggestion_id in favorite_suggestions:
        favorite_suggestions.remove(suggestion_id)
    
    with open('favorite_suggestions.txt', 'w') as f:
        for line in favorite_suggestions:
            f.write(line + '\n')
    
    return 'OK', 200

# Function to return a user's favorite outfit suggestions on the favorites page
@app.route('/favorites')
#@login_required
def favorites():
    email = session['email']
    user = User.query.filter_by(email=email).first()
    user_id = user.id

    # Initialize dictionary to store product suggestions grouped by user suggestion
    suggestion_products = {}

    # Read in favorited suggestions from file
    with open('favorite_suggestions.txt', 'r') as f:
        for line in f:
            suggestion_id = int(line.strip())

            # Retrieve user suggestion from the database based on suggestion ID
            suggestion = Suggestion.query.get(suggestion_id)

            # Check if the suggestion exists
            if suggestion:
                # Initialize list to store products for this suggestion
                suggestion_products[suggestion_id] = []

                # Match product names for each category
                categories = ['top', 'outerwear', 'hat', 'bottoms', 'socks', 'footwear', 'belt']
                for category in categories:
                    product_info = getattr(suggestion, category)  # Get product info from suggestion
                    if product_info:
                        # Parse the string to extract the product name
                        product_name = product_info.split(',')[0].strip("[]").strip('"').strip("'")
                        # Query the product table for the matching product
                        product = Product.query.filter_by(name=product_name).first()
                        if product:
                            suggestion_products[suggestion_id].append({
                                'name': product.name,
                                'price': product.price,
                                'color': product.color,
                                'image': product.image, 
                                'link': product.link,  
                            })
                        else:
                            # Skip if product doesn't exist
                            pass

    return render_template('favorites.html', suggestion_products=suggestion_products)

# Function to gather user's preferences 
@app.route('/pref', methods=['GET', 'POST'])
#@login_required
def pref():
    # Retreive user preferences from form
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
        age = '18'
        Style = request.form['Style']
        Season = request.form['Season']
        fabric = request.form['fabric']
        usersRequest = request.form['usersRequest']
        
        # Insert all the preferences to the DB
        email = session['email']
        user = User.query.filter_by(email=email).first()
        user_id = user.id
        query = UserQuery(user_id=user_id , gender=gender, weight=weight, waist=waist, length=length, Skintone=Skintone, height=height, hair=hair, build=build, Budget=Budget, Colors=Colors, age=age, Style=Style, Season=Season, fabric=fabric, usersRequest=usersRequest)
        db.session.add(query)
        db.session.commit()
        generated_id = query.id
        print(f'The generated ID for the newly inserted row is: {generated_id}')

        # Send the user query of their preferences to be run through the AI
        one_getUserData(generated_id=generated_id, gender=gender, weight=weight, waist=waist, length=length, Skintone=Skintone, height=height, hair=hair, build=build, Budget=Budget, Colors=Colors, age=age, Style=Style, Season=Season, fabric=fabric, usersRequest=usersRequest)
        
        resp = redirect(url_for('dashboard'))
        return resp
    return render_template('registerSize.html')

# Function to change user password 
@app.route('/userSettings', methods=['GET', 'POST'])
def user_settings():
    if request.method == 'POST':
        old_password = request.form.get('oldPassword')
        new_password = request.form.get('newPassword')
        confirm_password = request.form.get('confirmPassword')
        email = session['email']
        current_user = User.query.filter_by(email=email).first()

        # Check if the old password matches the stored password
        if not current_user.check_password(old_password):
            flash('Incorrect current password', 'error')
            return redirect(url_for('user_settings'))

        # Check if the new password matches the confirm password
        if new_password != confirm_password:
            flash('New password and confirm password do not match', 'error')
            return redirect(url_for('user_settings'))

        # Update the user's password in the database
        current_user.set_password(new_password)
        db.session.commit()

        flash('Password successfully updated', 'success')
        return render_template('userSettings.html')

    return render_template('userSettings.html')

# Function to log out the user
@app.route('/logout')
def logout():
    #logout_user()
    flash('You have been logged out!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5555)
