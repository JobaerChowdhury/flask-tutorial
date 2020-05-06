import os
import tempfile
import shutil

import pytest
from flaskr import create_app


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

    DATABASE = db_path
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///" + DATABASE,
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "UPLOAD_DIR": upload_path,
        }
    )

    with app.app_context():
        from flaskr.database import init_db, load_test_data

        init_db()
        load_test_data()

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
