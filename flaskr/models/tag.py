from flaskr import db


# Tag
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

    veokit_installation_id = db.Column(db.Integer, nullable=False, index=True)
