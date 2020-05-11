from app.database import db
from app.short_link_module.models import Link

user_links = db.Table("user_links",
                      db.Column("user_id", db.Integer,
                                db.ForeignKey("user.id")),
                      db.Column("link_id", db.Integer,
                                db.ForeignKey("link.id")))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    links = db.relationship("Link", secondary=user_links, lazy="dynamic")

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

    def __repr__(self):
        return f"<User id: {self.id}, username: {self.username}"
