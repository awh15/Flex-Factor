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

from .product_model import Product, product_schema, products_schema

user_app_url = 'http://localhost:5000/'
review_app_url = 'http://localhost:5200/'

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


@app.route("/search", methods=["POST"])
def search():
    if "search" not in request.json:
        abort(400, "No search request")
    s = Product.query.filter(or_(Product.name.ilike(request.json["search"]),
                                 Product.description.ilike(request.json["search"]))).all()
    return jsonify(products_schema.dump(s))


@app.route('/addproduct', methods=['POST'])
def add_product():
    if not ("name" in request.json and
            "description" in request.json and
            "price" in request.json and
            "stock" in request.json and
            "category" in request.json and
            "image" in request.json):
        abort(400)
    token = extract_auth_token(request)
    try:
        vendor_id = decode_token(token)
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        abort(403)
    #vendor_id = request.json["vendor_id"]
    name = request.json["name"]
    description = request.json["description"]
    price = request.json["price"]
    stock = request.json["stock"]
    category = request.json["category"]
    image = request.json["image"]

    # if not (vendor_id and name and description and price and stock and category and image):
    #     abort(400)
    
    # Check if profile is a vendor
    response = requests.post(user_app_url+'get_role')
    
    if not response:
        abort(400)
    
    role = response["role"]

    if role != "Vendor":
        abort(403)
    
    p = Product(vendor_id, name, description, price, stock, category, image, 0)

    db.session.add(p)
    db.session.commit()

    return jsonify(product_schema.dump(p)), 201

@app.route('/deleteproduct', methods=['POST'])
def delete_product():
    token = extract_auth_token(request)
    try:
        vendor_id = decode_token(token)
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        abort(403)
    product_id = request.json["product_id"]
    
    response = requests.post(user_app_url+'get_role')
    
    if not response:
        abort(400)
    
    role = response["role"]

    if role != "Vendor":
        abort(403)
    
    if not product_id:
        abort(400)

    requests.post(review_app_url+'delete_product_reviews', { "product_id": product_id })
    
    Product.query.filter_by(product_id=product_id).delete()

    db.session.commit()

    return {"Message": "Delete Successful"}, 200


@app.route('/changeproduct', methods=['POST'])
def change_product():
    token = extract_auth_token(request)
    try:
        vendor_id = decode_token(token)
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        abort(403)
    product_id = request.json["product_id"]
    description = request.json["description"]
    price = request.json["price"]
    stock = request.json["stock"]
    image = request.json["image"]
    
    response = requests.post(user_app_url+'get_role')
    
    if not response:
        abort(400)
    
    role = response["role"]

    if role != "Vendor":
        abort(403)

    if not product_id:
        abort(400)

    p = Product.query.filter_by(product_id=product_id).first()

    if not p:
        abort(400)

    # Change information
    if description: p.description = description
    if price: p.price = price
    if stock: p.stock = stock
    if image: p.image_url = image

    db.session.commit()

    return jsonify(product_schema.dump(p)), 200

@app.route('/product', methods=['POST'])
def get_product():
    # Product ID
    product = request.json["product_id"]

    if not product:
        abort(403)

    p = Product.query.filter_by(product_id=product).first()

    return jsonify(product_schema.dump(p))

if __name__ == '__main__':
    db.create_all()