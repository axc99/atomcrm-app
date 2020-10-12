from flask_babel import _
from flaskr import db
import enum
from sqlalchemy import Integer, Enum, Column


# Field type
class FieldType(enum.Enum):
    string = 1
    long_string = 2
    number = 3
    boolean = 4
    select = 5


# Field
class Field(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

    value_type = Column(Enum(FieldType), nullable=False)

    # Add lead field to lead title (ex: first_name, last_name, middle_name)
    as_title = db.Column(db.Boolean, default=False, nullable=False)

    # Primary field
    primary = db.Column(db.Boolean, default=False, nullable=False)

    # Min/max for string length and number
    min = db.Column(db.Integer, default=1, nullable=True)
    max = db.Column(db.Integer, nullable=True)

    index = db.Column(db.Integer, default=0, nullable=False)

    veokit_installation_id = db.Column(db.Integer, nullable=False, index=True)


def get_field_types():
    return (
        (1, 'string', _('m_status_getFieldTypes_string')),
        (2, 'long_string', _('m_status_getFieldTypes_longString')),
        (3, 'number', _('m_status_getFieldTypes_number')),
        (4, 'boolean', _('m_status_getFieldTypes_boolean')),
        (5, 'select', _('m_status_getFieldTypes_select'))
    )