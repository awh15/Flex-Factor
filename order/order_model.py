from .order_app import db, ma
import datetime
import json
from enum import Enum

'''
OrderID (Primary Key)
UserID
ProductIDS
TotalPrice
Status (Processing, Shipped, Delivered)
OrderDate
DeliveryDate
'''

class OrderStatus(str, Enum):
    CONFIRMED = 'Confirmed'
    RECEIEVED = 'Received'
    SHIPPED = 'Shipped'

class Order(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Numeric(10, 2))
    status = db.Column(db.String(20))
    order_date = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    delivery_date = db.Column(db.DateTime)

    def __init__(self, user_id, total_price, delivery_date):
        self.user_id = user_id
        self.total_price = total_price
        self.status = OrderStatus.CONFIRMED
        self.delivery_date = delivery_date

class OrderSchema(ma.Schema):
    class Meta:
        fields = ("order_id", "user_id", "total_price", "status", "order_date", "delivery_date")
        model = Order

order_schema = OrderSchema()