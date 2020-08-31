from flaskr import db
from datetime import datetime


# API Token
class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(300))
    active = db.Column(db.Boolean, default=True)

    add_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    veokit_system_id = db.Column(db.Integer, nullable=False)
