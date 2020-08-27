from flaskr import db
from datetime import datetime, date


# Lead
class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    add_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    upd_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    veokit_system_id = db.Column(db.Integer, nullable=False, index=True)


# Lead field
class LeadField(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    value = db.Column(db.String(1000), nullable=True)

    lead_id = db.Column(db.Integer, db.ForeignKey('lead.id', ondelete='SET NULL'), nullable=False)


# Lead tag
class LeadTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lead_id = db.Column(db.Integer, db.ForeignKey('lead.id', ondelete='SET NULL'), nullable=False)