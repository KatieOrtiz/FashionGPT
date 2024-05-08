from flask import request, render_template, redirect, url_for, session, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta, timezone
from flask_cors import CORS, cross_origin
from models import User, UserQuery, Suggestion
import jwt
from extensions import app, db, login_manager

from haiku import one_getUserData


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

        #sending query to AI
        one_getUserData(generated_id=generated_id, gender=gender, weight=weight, waist=waist, length=length, Skintone=Skintone, height=height, hair=hair, build=build, Budget=Budget, Colors=Colors, age=age, Style=Style, Season=Season, fabric=fabric, usersRequest=usersRequest)
        
        resp = redirect(url_for('dashboard'))
        return resp
    return render_template('reigstersize.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))












#################################################################################################################
# API only 
#################################################################################################################
# nothing to do with out project


@app.route('/api/register', methods=['POST'])
def register1():
    if request.method == 'POST':
        # Parse data from JSON request
        data = request.get_json()
        username = data['username']
        email = data['email']
        password = data['password']

        # Check if user already exists
        if User.query.filter_by(email=email).first():
            return jsonify({'message': 'Email already exists.'}), 409  # HTTP Conflict

        # Create new user
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email)
        new_user.set_password(password)

        # Add user to database
        db.session.add(new_user)
        db.session.commit()

        # Generate JWT token
        token = jwt.encode({
            'user': email,
            'exp': datetime.now(timezone.utc) + timedelta(minutes=10)
        }, app.secret_key, algorithm='HS256')

        # Return success response with token
        return jsonify({'token': token}), 201  # HTTP Created
    return jsonify({'message': 'Method not allowed'}), 405  # HTTP Method Not Allowed

@app.route('/api/login', methods=['POST'])
def login1():
    # Get data from JSON request
    data = request.get_json()
    user_identifier = data.get('emailOrUsername')
    password = data.get('password')

    if not user_identifier or not password:
        return jsonify({'message': 'Username/email and password are required.'}), 400  # Bad Request

    # Check if the identifier is an email or a username
    if "@" in user_identifier:  # Simple check to assume it's an email
        user = User.query.filter_by(email=user_identifier).first()
    else:
        user = User.query.filter_by(username=user_identifier).first()

    if user is None:
        return jsonify({'message': 'No account found with that identifier.'}), 404  # Not Found

    # Verify the password
    if user and user.check_password(password):
        # Generate JWT token
        token = jwt.encode({
            'user_id': user.id,  # It's often more useful to encode the user ID instead of email or username
            'exp': datetime.utcnow() + timedelta(minutes=10)
        }, app.secret_key, algorithm='HS256')

        # Return success response with token
        return jsonify({'token': token}), 200  # OK

    # If password does not match
    return jsonify({'message': 'Invalid credentials.'}), 401  # Unauthorized

@app.route('/api/user_queries', methods=['GET'])
def get_user_queries():
    # Retrieve token and user ID from the request's query parameters
    # token = request.args.get('token')
    user_id = request.args.get('user_id')

    # if not token or not user_id:
    #     return jsonify({'error': 'Token and user ID are required'}), 400

    # try:
    #     # Decode the JWT token
    #     decoded = jwt.decode(token, app.secret_key, algorithms=['HS256'])
    #     # Verify if the user ID in the JWT matches the provided user ID
    #     if str(decoded['user_id']) != user_id:
    #         return jsonify({'error': 'Unauthorized access'}), 403
    # except jwt.ExpiredSignatureError:
    #     return jsonify({'error': 'Token expired'}), 401
    # except jwt.InvalidTokenError:
    #     return jsonify({'error': 'Invalid token'}), 401

    # Fetch the user queries from the database
    try:
        # Fetch suggestions where user_id matches and choose is 'general'
        suggestions = Suggestion.query.filter_by(user_id=user_id, choose='general').all()
        print(suggestions)
        suggestions_data = [{
            'id': suggestion.id,
            'query_id': suggestion.query_id,
            'choose': suggestion.choose,
            'top': suggestion.top,
            'outerwear': suggestion.outerwear,
            'hat': suggestion.hat,
            'necklace': suggestion.necklace,
            'earring': suggestion.earring,
            'bottoms': suggestion.bottoms,
            'socks': suggestion.socks,
            'footwear': suggestion.footwear,
            'bracelet': suggestion.bracelet,
            'watch': suggestion.watch,
            'belt': suggestion.belt,
            'avgTotalPrice': suggestion.avgTotalPrice,
            'reasoning': suggestion.reasoning,
            'usersRequest': suggestion.usersRequest,
            'timestamp': suggestion.timestamp.isoformat() if suggestion.timestamp else None
        } for suggestion in suggestions]
        print(suggestions_data)

        return jsonify(suggestions_data), 200
    except Exception as e:
        app.logger.error(f"An error occurred: {str(e)}")
        return jsonify({'error': 'Could not fetch user queries'}), 500

@app.route('/api/update_user_data/<int:user_id>', methods=['GET', 'POST'])
def update_user_data(user_id):
    if request.method == 'POST':
        new_username = request.form.get('username')
        new_email = request.form.get('email')
        try:
            user = User.query.get(user_id)
            if user:
                user.username = new_username if new_username else user.username
                user.email = new_email if new_email else user.email
                db.session.commit()
                return jsonify({'message': 'User data updated successfully'}), 200
            else:
                return jsonify({'message': 'User not found'}), 404
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'Failed to update user data', 'error': str(e)}), 500
    else:  # GET request
        try:
            user = User.query.get(user_id)
            if user:
                return jsonify({
                    'user_id': user.id,
                    'username': user.username,
                    'email': user.email
                }), 200
            else:
                return jsonify({'message': 'User not found'}), 404
        except Exception as e:
            return jsonify({'message': 'Failed to retrieve user data', 'error': str(e)}), 500

@app.route('/api/delete_account/<int:user_id>', methods=['POST'])
def delete_account(user_id):
    try:
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify({'message': 'User account deleted successfully'}), 200
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to delete account', 'error': str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5555)
