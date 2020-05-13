import os

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY") or \
                 "Won't you fly hiigh, ooh free biiird yeah"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DEVELOPMENT_DATABASE_URI") or "sqlite:///" + os.path.join(basedir,
                                                                   "app.db")


class ReleaseConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("RELEASE_DATABASE_URI") \
                              or "sqlite:///" + os.path.join(basedir, "app.db")


class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TESTING_DATABASE_URI') or \
                              "sqlite:///" + os.path.join(basedir, "app.db")
