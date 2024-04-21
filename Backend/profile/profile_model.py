from .profile_app import db, ma

'''
ProfileID (Primary Key)
UserID (Foreign Key)
FullName
Address
PhoneNumber
'''

class Profile(db.Model):
    profile_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=True)
    full_name = db.Column(db.String(50))
    address = db.Column(db.String(100))
    phone_number = db.Column(db.String(20))

    def __init__(self, user_id, full_name, address, phone_number):
        self.user_id = user_id
        self.full_name = full_name
        self.address = address
        self.phone_number = phone_number

class ProfileSchema(ma.Schema):
    class Meta:
        fields = ("profile_id", "user_id", "full_name", "address", "phone_number")
        model = Profile

profile_schema = ProfileSchema()

