from .product_app import db, ma

'''
FAQID (Primary Key)
Question
Answer
Product ID
Language
'''

class FAQ(db.Model):
    faq_id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text)
    answer = db.Column(db.Text)
    product_id = db.Column(db.Integer)

    def __init__(self, question, answer, product_id):
        self.question = question
        self.answer = answer
        self.product_id = product_id

class FAQSchema(ma.Schema):
    class Meta:
        fields = ("faq_id", "question", "answer", "product_id")
        model = FAQ

faqs_schema = FAQSchema(many=True)
faq_schema = FAQSchema()