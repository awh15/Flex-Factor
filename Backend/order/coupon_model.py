from .order_app import db, ma

'''
CouponID (Primary Key)
Code
DiscountPercentage
ExpiryDate
UsageLimit
'''

class Coupon(db.Model):
    coupon_id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True)
    discount_percentage = db.Column(db.Float)
    expiry_date = db.Column(db.DateTime)
    usage_limit = db.Column(db.Integer)

    def __init__(self, code, discount_percentage, expiry_date, usage_limit):
        self.code = code
        self.discount_percentage = discount_percentage
        self.expiry_date = expiry_date
        self.usage_limit = usage_limit

class CouponSchema(ma.Schema):
    class Meta:
        fields = ("coupon_id", "code", "discount_percentage", "expiry_date", "usage_limit")
        model = Coupon

coupon_schema = CouponSchema()
