from flaskr import db
from datetime import datetime


# API Token
class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(300), nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)

    add_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    veokit_installation_id = db.Column(db.Integer, nullable=False)
