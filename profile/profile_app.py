import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask import abort
from db_config import DB_CONFIG
from secret_key import SECRET_KEY
import jwt
import requests

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONFIG+'profile'
CORS(app)
ma = Marshmallow(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from .profile_model import Profile, profile_schema


def decode_token(token):
    payload = jwt.decode(token, SECRET_KEY, 'HS256')
    return payload['sub']

def extract_auth_token(authenticated_request):
    auth_header = authenticated_request.headers.get('Authorization')
    if auth_header:
        return auth_header.split(" ")[1]
    else:
        return None

@app.route('/create_profile', methods=['POST'])
def create_profile():
    name = request.json["full_name"]
    address = request.json["address"]
    phone = request.json["phone_number"]
    user_id = request.json["user_id"]

    p = Profile(user_id, name, address, phone)
    db.session.add(p)
    db.session.commit()

    return jsonify(profile_schema.dump(p)), 201

@app.route("/update_profile", methods=["POST"])
def update_profile():
    token = extract_auth_token(request)
    try:
        user_id = decode_token(token)
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        abort(403)
    p = Profile.query.filter_by(user_id=user_id).first()
    if "full_name" in request.json: p.full_name = request.json["full_name"]
    if "address" in request.json: p.address = request.json["address"]
    if "phone_number" in request.json: p.phone_number = request.json["phone_number"]
    db.session.commit()
    return jsonify(profile_schema.dump(p))


@app.route("/get_profile", methods=["GET"])
def get_profile():
    user_id = request.json["id"]

    p = Profile.query.filter_by(user_id=user_id).first()
    
    if not p:
        abort(403)
    
    return jsonify(profile_schema.dump(p))

with app.app_context():
    db.create_all()