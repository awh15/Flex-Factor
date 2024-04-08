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
from .faq_model import FAQ, faq_schema, faqs_schema

user_app_url = 'http://localhost:5001/'
review_app_url = 'http://localhost:5200/'
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


@app.route("/search", methods=["POST"])
def search():
    if "search" not in request.json:
        abort(400, "No search request")
    s = Product.query.filter(or_(Product.name.ilike(request.json["search"]),
                                 Product.description.ilike(request.json["search"]))).all()
    return jsonify(products_schema.dump(s))


@app.route('/add', methods=['POST'])
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

    name = request.json["name"]
    description = request.json["description"]
    price = request.json["price"]
    stock = request.json["stock"]
    category = request.json["category"]
    image = request.json["image"]
    
    # Check if profile is a vendor
    response = requests.get(user_app_url+'get_role', json={"id":vendor_id})

    if response.status_code == 400:
        abort(400)

    role = response.json()["role"]

    if role != "Vendor":
        abort(403)
    
    p = Product(vendor_id, name, description, price, stock, category, image, 0)

    db.session.add(p)
    db.session.commit()

    return jsonify(product_schema.dump(p)), 201


@app.route('/delete', methods=['POST'])
def delete_product():
    token = extract_auth_token(request)
    try:
        vendor_id = decode_token(token)
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        abort(403)
    product_id = request.json["product_id"]
    
    response = requests.get(user_app_url+'get_role', json={"id":vendor_id})
    
    if not response:
        abort(400)
    
    role = response.json()["role"]

    if role != "Vendor":
        abort(403)
    
    if not product_id:
        abort(400)

    # Delete related Reviews and FAQs
    requests.post(review_app_url+'delete_product_reviews', json={"product_id": product_id})
    requests.post(product_app_url+'delete_product_faq', json={"product_id": product_id})
    
    Product.query.filter_by(product_id=product_id).delete()

    db.session.commit()

    return {"Message": "Delete Successful"}, 200


@app.route('/change', methods=['POST'])
def change_product():
    token = extract_auth_token(request)
    try:
        vendor_id = decode_token(token)
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        abort(403)

    description = None
    price = None
    stock = None
    image = None
    name = None
    
    if "product_id" not in request.json:
        abort(400)

    product_id = request.json["product_id"]

    if "name" in request.json: name = request.json["name"]
    
    if "description" in request.json: description = request.json["description"]
    
    if "price" in request.json: price = request.json["price"]
    
    if "stock" in request.json: stock = request.json["stock"]
    
    if "image" in request.json:
        image = request.json["image"]
    
    response = requests.get(user_app_url+'get_role', json={"id": vendor_id})
    
    if not response or response.json()["role"] != "Vendor":
        abort(400)

    p = Product.query.filter_by(product_id=product_id).first()

    if not p:
        abort(400)

    # Change information
    if name: p.name = name
    if description: p.description = description
    if price: p.price = price
    if stock: p.stock = stock
    if image: p.image_url = image

    db.session.commit()

    return jsonify(product_schema.dump(p)), 200


@app.route('/product', methods=['GET'])
def get_product():
    product = request.json["name"]

    if not product:
        abort(403)

    p = Product.query.filter_by(name=product).first()

    return jsonify(product_schema.dump(p))


@app.route('/list', methods=['GET'])
def get_products_list():
    # Get user id and check if vendor
    token = extract_auth_token(request)
    try:
        vendor_id = decode_token(token)
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        abort(403)

    response = requests.get(user_app_url+'get_role', json={"id": vendor_id})

    if response.json()["role"] != "Vendor":
        abort(400)

    # Return all associated products of vendor
    p = Product.query.filter_by(vendor_id=vendor_id).all()

    return jsonify(products_schema.dump(p))


@app.route('/faq', methods=['POST'])
def post_faq():
    token = extract_auth_token(request)
    try:
        vendor_id = decode_token(token)
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        abort(403)

    response = requests.get(user_app_url+'get_role', json={"id": vendor_id})

    # Only Vendor can set FAQs
    if response.json()["role"] != "Vendor":
        abort(400)
        
    if ("question" not in request.json and "answer" not in request.json and "product" not in request.json):
        abort(400)

    question = request.json["question"]
    answer = request.json["answer"]
    product = request.json["product"]
    
    p = Product.query.filter_by(name=product).first()

    if not p:
        abort(400)

    p = p.product_id

    # Duplicate questions for same product
    dup = FAQ.query.filter((FAQ.question == question) & (FAQ.product_id == p)).first()
    
    if dup:
        abort(400)

    f = FAQ(question, answer, p)

    db.session.add(f)
    db.session.commit()

    return jsonify(faq_schema.dump(f)), 201


@app.route('/faq', methods=['GET'])
def get_faq():
    if "name" not in request.json:
        abort(400)

    product = request.json["name"]

    p = Product.query.filter_by(name=product).first()

    if not p:
        abort(400)

    p = p.product_id

    f = FAQ.query.filter_by(product_id=p).all()

    return jsonify(faqs_schema.dump(f)), 200


@app.route('/delete_product_faq', methods=['POST'])
def delete_product_faq():
    # Delete all FAQs for product
    if "product_id" not in request.json:
        abort(400)
        
    product = request.json["product_id"]

    p = Product.query.filter_by(product_id=product).first()

    if not p:
        abort(400)

    p = p.product_id

    FAQ.query.filter_by(product_id=p).delete()

    db.session.commit()

    return {"message": "deleted product FAQ"}, 200


@app.route('/delete_faq', methods=['POST'])
def delete_faq():
    if "faq_id" not in request.json:
        abort(400)
    
    faq_id = request.json["faq_id"]

    FAQ.query.filter_by(faq_id=faq_id).delete()

    db.session.commit()

    return {"message": "deleted FAQ"}, 200


with app.app_context():
    db.create_all()