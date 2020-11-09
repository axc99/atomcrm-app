from flask_babel import _
from flaskr import db
import enum
from datetime import datetime, date
from sqlalchemy import Integer, Enum, Column


# Status color
class StatusColor(enum.Enum):
    red = 1
    pink = 2
    purple = 3
    blue = 4
    green = 5
    orange = 6


# Status
class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    color = Column(Enum(StatusColor), nullable=False)

    name = db.Column(db.String(30), nullable=False)
    index = db.Column(db.Integer, default=0, nullable=False)

    nepkit_installation_id = db.Column(db.Integer, nullable=False, index=True)


# Get HEX color by color key
def get_hex_by_color(color_key):
    status_colors = get_status_colors()
    return next((c[2] for c in status_colors if c[1] == color_key), None)


def get_status_colors():
    return (
        (1, 'red', '#E57373', _('m_status_getStatusColors_red')),
        (2, 'pink', '#F48FB1', _('m_status_getStatusColors_pink')),
        (3, 'purple', '#9575CD', _('m_status_getStatusColors_purple')),
        (4, 'blue', '#64B5F6', _('m_status_getStatusColors_blue')),
        (5, 'green', '#81C784', _('m_status_getStatusColors_green')),
        (6, 'orange', '#FFA726', _('m_status_getStatusColors_orange'))
    )
