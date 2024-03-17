from ..app import db, ma, bcrypt
import datetime

'''
TransactionID (Primary Key)
OrderID (Foreign Key)
PaymentMethod
TransactionDate
Amount
'''

class Transaction(db.Model):
    transaction_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.order_id'), nullable=False)
    payment_method = db.Column(db.String(30))
    transaction_date = db.Column(db.DateTime, default=datetime.utcnow)
    amount = db.Column(db.Numeric(10, 2))

    order = db.relationship('Order', backref=db.backref('transaction', uselist=False, lazy=True))

    def __init__(self, order_id, payment_method, amount):
        self.order_id = order_id
        self.payment_method = payment_method
        self.amount = amount

class TransactionSchema(ma.Schema):
    class Meta:
        fields = ("transaction_id", "order_id", "payment_method", "transaction_date", "amount")
        model = Transaction

transaction_schema = TransactionSchema()
