from .product_app import db, ma

'''
FAQID (Primary Key)
Question
Answer
Language
'''

class FAQ(db.Model):
    faq_id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text)
    answer = db.Column(db.Text)
    language = db.Column(db.String(20))

    def __init__(self, question, answer, language):
        self.question = question
        self.answer = answer
        self.language = language

class FAQSchema(ma.Schema):
    class Meta:
        fields = ("faq_id", "question", "answer", "language")
        model = FAQ

faq_schema = FAQSchema()
