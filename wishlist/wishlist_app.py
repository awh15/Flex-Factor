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

from .wishlist_model import Wishlist, wishlist_schema

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


@app.route("/add_wishlist", methods=["POST"])
def add_to_wishlist():
    token = extract_auth_token(request)
    try:
        user_id = decode_token(token)
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        abort(403)
    if "product_id" not in request.json:
        abort(400, "Missing product id")
    existing_item = Wishlist.query.filter_by(user_id=user_id, product_id=request.json["product_id"]).first()
    if existing_item:
        return jsonify({'message': 'This item is already in your wishlist.'}), 400
    
    wish = Wishlist(user_id=user_id, product_id=request.json["product_id"])
    db.session.add(wish)
    db.session.commit()

    return jsonify({'message': 'Product added to wishlist successfully.'})

@app.route("/wishlist", methods=["GET"])
def get_wishlist():
    token = extract_auth_token(request)
    try:
        user_id = decode_token(token)
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        abort(403)
    items = Wishlist.query.filter_by(user_id=user_id).all()

    return jsonify(wishlist_schema.dump(items))


if __name__ == '__main__':
    db.create_all()