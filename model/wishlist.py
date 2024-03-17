from ..app import db, ma, bcrypt

'''
WishlistID (Primary Key)
UserID (Foreign Key)
ProductID (Foreign Key)
'''

class Wishlist(db.Model):
    wishlist_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)

    user = db.relationship('User', backref=db.backref('wishlist', lazy=True))
    product = db.relationship('Product', backref=db.backref('wishlist', lazy=True))

    def __init__(self, user_id, product_id):
        self.user_id = user_id
        self.product_id = product_id

class WishlistSchema(ma.Schema):
    class Meta:
        fields = ("wishlist_id", "user_id", "product_id")
        model = Wishlist

wishlist_schema = WishlistSchema()
