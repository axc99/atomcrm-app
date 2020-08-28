from flaskr import db
from secrets import choice
import string


# API Token
class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(300))
    active = db.Column(db.Boolean, default=True)

    veokit_system_id = db.Column(db.Integer, nullable=False)
