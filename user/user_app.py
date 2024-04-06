import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask import abort
from db_config import DB_CONFIG
from secret_key import SECRET_KEY
import jwt
import requests

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONFIG
CORS(app)
ma = Marshmallow(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from .user_model import User, user_schema, UserRole

profile_app_url = 'http://localhost:5050/'

@app.route('/register', methods=['POST'])
def register():
    username = request.json["username"]
    password = request.json["password"]
    role = request.json["role"]
    email = request.json["email"]
    name = request.json["full_name"]
    address = request.json["address"]
    phone_number = request.json["phone_number"]

    # User Sanitization
    if not (username and password and role and email and name and address and phone_number):
        return jsonify({"Message": "Please fill all missing fields"}), 400
    
    username_exists = User.query.filter_by(username=username).all()
    if username_exists:
        return jsonify({"Message": "Username exists"}), 406
    
    email_exists = User.query.filter_by(email=email).all()
    if email_exists:
        return jsonify({"Message": "Email already in use"}), 406
    
    # Create user and add to db
    u = User(username, password, email, role)

    db.session.add(u)
    db.session.commit()

    # Create user profile
    create_profile_payload = {
        "full_name": name,
        "address": address,
        "phone_number": phone_number,
        "user_id": u.user_id
    }

    response = requests.post(profile_app_url+'create_profile', json=create_profile_payload)

    if response == 201:
        return jsonify(user_schema.dump(u)), 201
    else:
        abort(400)


def extract_auth_token(authenticated_request):
    auth_header = authenticated_request.headers.get('Authorization')
    if auth_header:
        return auth_header.split(" ")[1]
    else:
        return None
    
    
def decode_token(token):
    payload = jwt.decode(token, SECRET_KEY, 'HS256')
    return payload['sub']


def create_token(user_id):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=4),
        'iat': datetime.datetime.utcnow(),
        'sub': user_id
    }
    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm='HS256'
    )


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

    return jsonify({"token": create_token(user.user_id)})


@app.route("/get_role", methods=["GET"])
def get_role():
    token = extract_auth_token(request)
    try:
        user_id = decode_token(token)
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        abort(403)
    u = User.query.filter_by(user_id=user_id).first()
    return jsonify({"role": u.role.value})


if __name__ == '__main__':
    db.create_all()
