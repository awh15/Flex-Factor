from .user_app import db, ma, bcrypt
from enum import Enum

'''
UserID (Primary Key)
Username
Password
Email
Role (Vendor, End User, Admin)
LanguagePreference
'''

class UserRole(str, Enum):
    VENDOR = "Vendor"
    END_USER = "End User"
    ADMIN = "Admin"

class LanguagePreference(Enum):
    ENGLISH = "English"
    ARABIC = "Arabic"

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    hashed_password = db.Column(db.String(128))
    email = db.Column(db.String(40), unique=True)
    role = db.Column(db.Enum(UserRole))
    language_preference = db.Column(db.Enum(LanguagePreference))

    def __init__(self, username, password, email, role):
        super(User, self).__init__(username=username, email=email, role=UserRole(role).name)
        self.hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

class UserSchema(ma.Schema):
    class Meta:
        fields = ("user_id", "username", "hashed_password", "email", "role", "language_preference")
        model = User

user_schema = UserSchema()
