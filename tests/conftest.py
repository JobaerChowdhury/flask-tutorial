import os
import tempfile
import shutil

import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db

db_file_path = os.path.join(os.path.dirname(__file__), "data.sql")
with open(db_file_path, "rb") as f:
    _data_sql = f.read().decode("utf8")


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username="test", password="test"):
        return self._client.post(
            "/auth/login", data={"username": username, "password": password}
        )

    def logout(self):
        return self._client.get("/auth/logout")


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    upload_path = tempfile.mkdtemp()

    app = create_app({"TESTING": True, "DATABASE": db_path, "UPLOAD_DIR": upload_path})

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)
    shutil.rmtree(upload_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def auth(client):
    return AuthActions(client)
