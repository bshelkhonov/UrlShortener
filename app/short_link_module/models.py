from datetime import datetime
from app.database import db


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_link = db.Column(db.String(140), unique=True)
    short_link = db.Column(db.String(20), unique=True)
    created = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, *args, **kwargs):
        super(Link, self).__init__(*args, **kwargs)

    def __repr__(self):
        return f"<Link id: {self.id}, title: {self.original_link}"
