from extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(512), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    api_requests = db.relationship('APIRequest', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class APIRequest(db.Model):
    __tablename__ = 'api_requests'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    request_type = db.Column(db.String(50), nullable=False)
    request_details = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class UserQuery(db.Model):
    __tablename__ = 'user_query'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    gender = db.Column(db.String)
    weight = db.Column(db.String)
    waist = db.Column(db.String)
    length = db.Column(db.String)
    Skintone = db.Column(db.String)
    height = db.Column(db.String)
    hair = db.Column(db.String)
    build = db.Column(db.String)
    Budget = db.Column(db.String)
    Colors = db.Column(db.String)
    age = db.Column(db.Integer)
    Style = db.Column(db.String)
    Season = db.Column(db.String)
    fabric = db.Column(db.String)
    usersRequest = db.Column(db.String)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Suggestion(db.Model):
    __tablename__ = 'user_suggestions'
    id = db.Column(db.Integer, primary_key=True)
    query_id = db.Column(db.Integer, db.ForeignKey('user_query.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    choose = db.Column(db.String)
    top = db.Column(db.String)
    outerwear = db.Column(db.String)
    hat = db.Column(db.String)
    necklace = db.Column(db.String)
    earring = db.Column(db.String)
    bottoms = db.Column(db.String)
    socks = db.Column(db.String)
    footwear = db.Column(db.String)
    bracelet = db.Column(db.String)
    watch = db.Column(db.String)
    belt = db.Column(db.String)
    avgTotalPrice = db.Column(db.String)
    reasoning = db.Column(db.String)
    usersRequest = db.Column(db.String)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float)
    color = db.Column(db.Text)  # Text type to handle multiple colors if stored as JSON
    image = db.Column(db.Text)
    link = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return f"<Product(name={self.name}, price={self.price}, color={self.color})>"
