import os

from flask import Flask

from .database import db
from .login_manager import lm
from .short_link_module.controllers import \
    short_link_module
from .users_module.controllers import users_module
import config


def create_app():
    app = Flask(__name__)
    app.secret_key = "Won't you fly hiigh, ooh free biiird yeah"

    if "APP_SETTINGS" in os.environ:
        app.config.from_object(os.environ["APP_SETTINGS"])
    else:
        app.config.from_object(config.ReleaseConfig)

    db.init_app(app)
    lm.init_app(app)

    with app.test_request_context():
        db.create_all()

    app.register_blueprint(short_link_module)
    app.register_blueprint(users_module)


    return app
