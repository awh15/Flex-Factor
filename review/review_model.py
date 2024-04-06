from .review_app import db, ma, bcrypt
from datetime import datetime

'''
ReviewID (Primary Key)
ProductID (Foreign Key)
UserID (Foreign Key)
Rating
Comment
ReviewDate
'''

class Review(db.Model):
    review_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    rating = db.Column(db.Integer)
    comment = db.Column(db.Text)
    review_date = db.Column(db.DateTime, default=datetime.utcnow)

    product = db.relationship('Product', backref=db.backref('reviews', lazy=True))
    user = db.relationship('User', backref=db.backref('reviews', lazy=True))

    def __init__(self, product_id, user_id, rating, comment):
        self.product_id = product_id
        self.user_id = user_id
        self.rating = rating
        self.comment = comment

class ReviewSchema(ma.Schema):
    class Meta:
        fields = ("review_id", "product_id", "user_id", "rating", "comment", "review_date")
        model = Review

review_schema = ReviewSchema()
