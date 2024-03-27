import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
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
from .model.profile import Profile, profile_schema
from .model.product import Product, products_schema

@app.route('/register', methods=['POST'])
def register():
    username = request.json["username"]
    password = request.json["password"]
    role = request.json["role"]
    email = request.json["email"]
    name = request.json["full_name"]
    address = request.json["address"]
    phone_number = request.json["phone_number"]

    if not (username and password and role and email and name and address and phone_number):
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
    
    p = Profile(u.user_id, name, address, phone_number)
    db.session.add(p)
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
        return jsonify({"Message": "User Login Successful"}), 200

    elif user.role == UserRole.VENDOR:
        return jsonify({"Message": "Vendo Login Successful"}), 200

    return abort(409, "Something went wrong")

@app.route("/profile", methods=["POST"])
def profile():
    if "username" not in request.json:
        abort(400, "Include username in request")
    u = User.query.filter_by(username=request.json["username"]).first()
    if not u:
        abort(400, "Username not found")
    p = Profile.query.filter_by(user_id=u.user_id).first()
    return jsonify(profile_schema.dump(p))


@app.route("/update_profile", methods=["POST"])
def update_profile():
    if "username" not in request.json:
        abort(400, "Include username in request")
    u = User.query.filter_by(username=request.json["username"]).first()
    if not u:
        abort(400, "Username not found")
    p = Profile.query.filter_by(user_id=u.user_id).first()
    if "full_name" in request.json: p.full_name = request.json["full_name"]
    if "address" in request.json: p.address = request.json["address"]
    if "phone_number" in request.json: p.phone_number = request.json["phone_number"]
    db.session.commit()
    return jsonify(profile_schema.dump(p))

    
@app.route("/search", methods=["POST"])
def search():
    if "search" not in request.json:
        abort(400, "No search request")
    s = Product.query.filter(or_(Product.name.ilike(request.json["search"]),
                                 Product.description.ilike(request.json["search"]))).all()
    return jsonify(products_schema.dump(s))

@app.route("/wishlist/<int:product_id>", methods=["POST"])
def add_to_wishlist():
    existing_item = Wishlist.query.filter_by(user_id=request.json["user_id"], product_id=product_id).first()
    if existing_item:
        return jsonify({'message': 'This item is already in your wishlist.'}), 400
    
    wish = Wishlist(user_id=request.json["user_id"], product_id=product_id)
    db.session.add(wish)
    db.session.commit()

    return jsonify({'message': 'Item added to wishlist successfully.'})

@app.route("/wishlist", methods=["GET"])
def get_wishlist():
    items = Wishlist.query.filter_by(user_id=request.json["user_id"])

    wl = [item.product_id for item in items]

    return jsonify(wl)