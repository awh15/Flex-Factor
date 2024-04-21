import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask import abort
from ..db_config import DB_CONFIG
from ..secret_key import SECRET_KEY
import jwt
import requests

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONFIG+'review'
CORS(app)
ma = Marshmallow(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from .review_model import Review, review_schema

user_app_url = "http://localhost:5001/"

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

@app.route('/add', methods=['POST'])
def add_review():
    token = extract_auth_token(request)
    try:
        user_id = decode_token(token)
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        abort(403)

    # Only End Users can add reviews
    u = requests.get(user_app_url+'get_role', json={'id':user_id})

    if u.status_code == 400 or u.json()["role"] != "End User":
        abort(400)

    product_id = request.json["product_id"]
    comment = request.json["comment"]
    rating = request.json["rating"]

    r = Review(product_id, user_id, rating, comment, datetime.datetime.utcnow())

    db.session.add(r)
    db.session.commit()

    return jsonify(review_schema.dump(r))

@app.route('/delete_review', methods=['POST'])
def delete_review():
    token = extract_auth_token(request)
    try:
        user_id = decode_token(token)
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        abort(403)

    product_id = request.json["product_id"]
    comment = request.json["comment"]
    rating = request.json["rating"]
    date = request.json["date"]

    Review.query.filter_by(product_id=product_id, comment=comment, rating=rating, review_date=date).delete()
    
    db.session.commit()
    
    return {"message": "deleted"}, 200


@app.route('/reviews', methods=['GET'])
def get_product_reviews():
    product_id = request.json["product_id"]

    return Review.query.filter_by(product_id=product_id)


@app.route('/delete_product_reviews', methods=['POST'])
def delete_product_reviews():
    product_id = request.json["product_id"]
    
    Review.query.filter_by(product_id=product_id).delete()
    
    db.session.commit()
    
    return {"Message": "deleted product reviews"}, 200


with app.app_context():
    db.create_all()