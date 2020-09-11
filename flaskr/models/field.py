from flaskr import db
import enum
from sqlalchemy import Integer, Enum, Column


# Field type
class FieldType(enum.Enum):
    string = 1
    number = 2
    boolean = 3
    select = 4


# Field
class Field(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

    value_type = Column(Enum(FieldType), nullable=False)

    # Add lead field to lead title (ex: first_name, last_name, middle_name)
    as_title = db.Column(db.Boolean, default=False, nullable=True)

    # Primary field
    primary = db.Column(db.Boolean, default=False, nullable=True)

    # Min/max for string length and number
    min = db.Column(db.Integer, default=1, nullable=True)
    max = db.Column(db.Integer, nullable=True)

    index = db.Column(db.Integer, default=0, nullable=True)

    veokit_installation_id = db.Column(db.Integer, nullable=False, index=True)
