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
    return next((c['hex'] for c in status_colors if c['key'] == color_key), None)


def get_status_colors():
    return [
        {'id': 1, 'key': 'red', 'hex': '#E57373', 'name': _('m_status_getStatusColors_red')},
        {'id': 2, 'key': 'pink', 'hex': '#F48FB1', 'name': _('m_status_getStatusColors_pink')},
        {'id': 3, 'key': 'purple', 'hex': '#9575CD', 'name': _('m_status_getStatusColors_purple')},
        {'id': 4, 'key': 'blue', 'hex': '#64B5F6', 'name': _('m_status_getStatusColors_blue')},
        {'id': 5, 'key': 'green', 'hex': '#81C784', 'name': _('m_status_getStatusColors_green')},
        {'id': 6, 'key': 'orange', 'hex': '#FFA726', 'name': _('m_status_getStatusColors_orange')}
    ]
