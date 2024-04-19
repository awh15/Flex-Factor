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

from .order_model import Order, order_schema
from .orderDetail_model import OrderDetail, order_detail_schema

product_app_url = 'http://localhost:5100/'

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


@app.route('/order', methods=['POST'])
def place_order():
    if not("product_id" in request.json and "quantity" in request.json):
        return {"Message": "Invalid request"}, 400

    token = extract_auth_token(request)
    try:
        vendor_id = decode_token(token)
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        abort(403)

    product_id = request.json["product_id"]
    quantity = request.json["quantity"]

    


@app.route('/cancel', mehtods=['POST'])
def cancel_order():
    pass


@app.route('/order', methods=['GET'])
def get_order():
    pass


