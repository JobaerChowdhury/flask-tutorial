import sqlite3

import pytest

from flaskr.db import get_db


def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute("SELECT 1")

    assert "closed" in str(e.value)


def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr("flaskr.db.init_db", fake_init_db)
    result = runner.invoke(args=["init-db"])
    assert "Initialized" in result.output
    assert Recorder.called


def test_load_test_data_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_load_test_data():
        Recorder.called = True

    monkeypatch.setattr("flaskr.db.load_test_data", fake_load_test_data)
    result = runner.invoke(args=["load-test-data"])
    assert "Loaded some test data" in result.output
    assert Recorder.called
