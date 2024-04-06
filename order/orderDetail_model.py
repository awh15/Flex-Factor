from ...app import db, ma, bcrypt

'''
OrderDetailID (Primary Key)
OrderID (Foreign Key)
ProductID (Foreign Key)
Quantity
Price
'''

class OrderDetail(db.Model):
    order_detail_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.order_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Numeric(10, 2))

    order = db.relationship('Order', backref=db.backref('order_details', lazy=True))
    product = db.relationship('Product', backref=db.backref('order_details', lazy=True))

    def __init__(self, order_id, product_id, quantity, price):
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.price = price

class OrderDetailSchema(ma.Schema):
    class Meta:
        fields = ("order_detail_id", "order_id", "product_id", "quantity", "price")
        model = OrderDetail

order_detail_schema = OrderDetailSchema()
