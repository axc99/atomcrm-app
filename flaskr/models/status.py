from flaskr import db
import enum
from datetime import datetime, date
from sqlalchemy import Integer, Enum, Column


# Status color
class StatusColor(enum.Enum):
    red = 1  # E57373
    pink = 2  # F48FB1
    purple = 3  # 9575CD
    blue = 4  # 64B5F6
    green = 5  # 81C784
    orange = 6  # FFA726


# Status
class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    color = Column(Enum(StatusColor), nullable=False)

    name = db.Column(db.String(20), nullable=False)
    index = db.Column(db.Integer, default=0, nullable=True)

    veokit_installation_id = db.Column(db.Integer, nullable=False, index=True)


# Get HEX color by color key
def get_hex_by_color(color):
    color_map = {
        'red': '#E57373',
        'pink': '#F48FB1',
        'purple': '#9575CD',
        'blue': '#64B5F6',
        'green': '#81C784',
        'orange': '#FFA726'
    }

    return color_map[color]
