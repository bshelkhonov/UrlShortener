import os
import tempfile

import unittest
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from app.short_link_module.controllers import short_link_module
from app.users_module.controllers import users_module


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.db_fd, self.app.config["DATABASE"] = tempfile.mkstemp()
        self.app.config["TESTIN"] = True

        self.db = SQLAlchemy()
        self.db.init_app(self.app)
        self.test_app = self.app.test_client()

        self.app.register_blueprint(short_link_module)
        self.app.register_blueprint(users_module)

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.app.config["DATABASE"])

    def login(self, username, password):
        return self.test_app.post('/login', data=dict(
            login=username,
            password=password
        ), follow_redirects=True)

    def register(self, username, password):
        return self.test_app.post('/register', data=dict(
            login=username,
            password=password
        ), follow_redirects=True)

    def test_not_empty(self):
        rv = self.test_app.get("/")
        assert rv.data

    def test_register(self):
        rv = self.register("admin", "1234")
        assert rv.data

    def test_redirect(self):
        rv = self.test_app.get("/history")
        assert "Redirecting..." in rv.data.decode()

    def test_history(self):
        self.register("admin", "1234")
        self.login("admin", "1234")
        rv = self.test_app.post("/", data=dict(link="http://example.com/"))
        rv = self.test_app.get("/history")
        assert "История" in rv.data.decode()
        assert "http://example.com/" in rv.data.decode()


if __name__ == '__main__':
    unittest.main()
