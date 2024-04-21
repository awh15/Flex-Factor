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

app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONFIG+'order'
CORS(app)
ma = Marshmallow(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from .order_model import Order, order_schema, orders_schema
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
    if not("product_id" in request.json and "quantity" in request.json and "date" in request.json):
        return {"Message": "Invalid request"}, 400

    token = extract_auth_token(request)
    try:
        user_id = decode_token(token)
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        abort(403)

    product_id = request.json["product_id"]
    quantity = request.json["quantity"]
    date = request.json["date"]

    response = requests.get(product_app_url+'availability', json={"id":product_id, "quantity": quantity}).json()

    # Get the price
    price = response["price"]

    # Update product details
    response = requests.get(product_app_url+'order_product', json={"id":product_id, "quantity": quantity})

    # Set the order
    if response.status_code == 200:
        order = Order(user_id, price, date)

        db.session.add(order)
        db.session.commit()

        return jsonify(order_schema.dump(order)), 201
    
    else:
        abort(400)


@app.route('/cancel', methods=['POST'])
def cancel_order():
    order_id = request.json["order_id"]

    order = OrderDetail.query.filter_by(order_id=order_id).all()

    if not order:
        abort(404)

    for o in order:
        response = requests.post(product_app_url+'cancel_order', json={"id":o.product_id, "quantity": o.quantity})

        if response.status_code != 200:
            abort(400)

        o.delete()

    Order.query.filter_by(id=order_id).delete()

    return {"Message": "Order cancelled"}, 200


@app.route('/order', methods=['GET'])
def get_order():
    token = extract_auth_token(request)
    try:
        user_id = decode_token(token)
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        abort(403)
    
    o = Order.query.filter_by(user_id=user_id).all()
    return jsonify(orders_schema.dump(o))


with app.app_context():
    db.create_all()