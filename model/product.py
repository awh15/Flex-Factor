from ..app import db, ma, bcrypt

'''
ProductID (Primary Key)
VendorID (Foreign Key)
Name
Description
Price
StockQuantity
Category
ImageURL
Rating
'''

class Product(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    vendor_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    name = db.Column(db.String(50))
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2))
    stock_quantity = db.Column(db.Integer)
    category = db.Column(db.String(30))
    image_url = db.Column(db.String(100))
    rating = db.Column(db.Float)

    vendor = db.relationship('User', backref=db.backref('products', lazy=True))

    def __init__(self, vendor_id, name, description, price, stock_quantity, category, image_url, rating):
        self.vendor_id = vendor_id
        self.name = name
        self.description = description
        self.price = price
        self.stock_quantity = stock_quantity
        self.category = category
        self.image_url = image_url
        self.rating = rating

class ProductSchema(ma.Schema):
    class Meta:
        fields = ("product_id", "vendor_id", "name", "description", "price", "stock_quantity", "category", "image_url", "rating")
        model = Product

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)