from flask_login import UserMixin

from app.database import db
from app.login_manager import lm

user_links = db.Table("user_links",
                      db.Column("user_id", db.Integer,
                                db.ForeignKey("user.id")),
                      db.Column("link_id", db.Integer,
                                db.ForeignKey("link.id")))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    links = db.relationship("Link", secondary=user_links, lazy="dynamic")

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

    def __repr__(self):
        return f"<User id: {self.id}, username: {self.username}"


@lm.user_loader
def load_user(user_id):
    return User.query.get(user_id)
