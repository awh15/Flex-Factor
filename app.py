import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask import abort
from .db_config import DB_CONFIG

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONFIG
CORS(app)
ma = Marshmallow(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from .model.user import User, user_schema, UserRole
from .model.product import Product, product_schema
from .model.review import Review, review_schema

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

    return jsonify(user_schema.dump(u)), 201

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

@app.route('/addproduct', methods=['POST'])
def add_product():
    vendor_id = request.json["vendor_id"]
    description = request.json["description"]
    price = request.json["price"]
    stock = request.json["stock"]
    category = request.json["category"]
    image = request.json["image"]

    if not (vendor_id and description and price and stock and category and image):
        return
    
    # Check if profile is a vendor
    v = User.query.filter_by(user_id=vendor_id).first()

    if not v or v.role != UserRole.VENDOR:
        abort(403)
    
    p = Product(vendor_id, v.username, description, price, stock, category, image, 0)

    db.session.add(p)
    db.session.commit()

    return jsonify(product_schema.dump(p)), 201


@app.route('/deleteproduct', methods=['POST'])
def delete_product():
    product_id = request.json["product_id"]

    if not product_id:
        abort(403)
        
    Review.query.filter_by(product_id=product_id).delete()
    Product.query.filter_by(product_id=product_id).delete()

    db.session.commit()

    return {"Message": "Delete Successful"}, 200

@app.route('/changeproduct', methods=['POST'])
def change_product():
    product_id = request.json["product_id"]
    description = request.json["description"]
    price = request.json["price"]
    stock = request.json["stock"]
    category = request.json["category"]
    image = request.json["image"]
    rating = request.json["rating"]

    if not product_id:
        abort(403)

    p = Product.query.filter_by(product_id=product_id).first()

    if not p:
        abort(403)

    # Change information
    if description: p.description = description
    if price: p.price = price
    if stock: p.stock = stock
    if category: p.category = category
    if image: p.image = image

    # Update Rating by calculating all reviews with that product id
    r = Review.query.filter_by(product_id=product_id).all()

    if rating>=0 and len(r) > 0:
        n = len(r) + 1          # To account for the new rating as well
        s = 0
        for i in r:
            s += i.rating/n
        s+=rating/n

        p.rating = s

    elif rating>=0 and len(r) == 0:
        p.rating = rating

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