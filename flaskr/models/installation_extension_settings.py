import random
import string
from flask_babel import _
from flaskr import db
from sqlalchemy.dialects.postgresql import JSONB
import enum
from sqlalchemy import Integer, Enum, Column


# Installation extension settings
class InstallationExtensionSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    token = db.Column(db.String(32), nullable=False)
    veokit_installation_id = db.Column(db.Integer, nullable=False, index=True)
    extension = db.Column(db.String(32), nullable=False)

    data = db.Column(JSONB, nullable=False)

    # Generate token
    @staticmethod
    def generate_token():
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))
