import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask import abort
from db_config import DB_CONFIG

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONFIG
CORS(app)
ma = Marshmallow(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from model.user import User, user_schema, UserRole

@app.route('/register', methods=['POST'])
def register():
    username = request.json["username"]
    password = request.json["password"]
    role = request.json["role"]
    email = request.json["email"]

    if not (username and password and role and email):
        return jsonify({"Message": "Please fill all missing fields"}), 400
    
    username_exists = User.query.filter_by(username=username).all()
    if username_exists:
        return jsonify({"Message": "Username exists"}), 406
    
    email_exists = User.query.filter_by(email=email).all()
    if email_exists:
        return jsonify({"Message": "Email already in use"}), 406

    u = User(username, password, email, role)

    db.session.add(u)
    db.session.commit()

    return jsonify({user_schema.dump(u)}), 201

@app.route('/login', methods=['POST'])
def login():
    username = request.json["username"]
    password = request.json["password"]

    if not (username and password):
        return jsonify({"Message": "Please fill all missing fields"}), 400
    
    user = User.query.filter_by(username=username).first()

    if not user:
        abort(403, "Wrong username or password")

    pass_check = bcrypt.check_password_hash(user.hashed_password, password)

    if not pass_check:
        abort(403, "Wrong username or password")

    # Check for user role and return accordingly
    if user.role == UserRole.ADMIN:
        return jsonify({"Message": "Admin Login Successful"}), 200
    
    elif user.role == UserRole.END_USER:
        jsonify({"Message": "User Login Successful"}), 200

    elif user.role == UserRole.VENDOR:
        jsonify({"Message": "Vendo Login Successful"}), 200

    return abort(409, "Something went wrong")

