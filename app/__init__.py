import os
from flask import Flask
from .database import db
from .short_link_module.controllers import module as short_link_module
import config


def create_app():
    app = Flask(__name__)
    if "APP_SETTINGS" in os.environ:
        app.config.from_object(os.environ["APP_SETTINGS"])
    else:
        app.config.from_object(config.ReleaseConfig)
    db.init_app(app)

    with app.test_request_context():
        db.create_all()

    app.register_blueprint(short_link_module)

    return app
