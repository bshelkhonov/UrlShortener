import os
import tempfile
import os

import unittest

from app import create_app
from app.users_module.models import User
from app.short_link_module.models import Link
import config

basedir = os.path.abspath(os.path.dirname(__file__))


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, self.db_file = tempfile.mkstemp()

        self.previous = os.environ.get("APP_SETTINGS")
        os.environ["APP_SETTINGS"] = "config.TestingConfig"

        config.TestingConfig.SQLALCHEMY_DATABASE_URI = "sqlite:///" + \
                                                       self.db_file

        self.app = create_app()
        self.test_app = self.app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.db_file)
        if self.previous is None:
            del os.environ["APP_SETTINGS"]
        else:
            os.environ["APP_SETTINGS"] = self.previous

    def send_link(self, url):
        return self.test_app.post("/", data=dict(link=url),
                                  follow_redirects=True)

    def login(self, username, password):
        return self.test_app.post("/login", data=dict(
            login=username,
            password=password
        ), follow_redirects=True)

    def register(self, username, password):
        return self.test_app.post("/register", data=dict(
            login=username,
            password=password
        ), follow_redirects=True)

    def test_short_link(self):
        url = "https://example.com"
        self.send_link(url)

        with self.app.app_context():
            assert len(Link.query.all()) == 1
            assert Link.query.first().original_link == url

    def test_register(self):
        rv = self.register("admin", "1234")
        with self.app.app_context():
            assert len(User.query.all()) > 0
            assert User.query.first().username == "admin"

    def test_redirect(self):
        rv = self.test_app.get("/history")
        assert "Redirecting..." in rv.data.decode()

    def test_history(self):
        self.register("admin", "1234")
        self.login("admin", "1234")
        self.send_link("http://example.com/")
        rv = self.test_app.get("/history")
        assert "История" in rv.data.decode()
        assert "http://example.com/" in rv.data.decode()


if __name__ == '__main__':
    unittest.main()
