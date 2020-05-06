import sqlite3

import pytest


def test_get_close_db(app):
    # Todo Is it possible to test if the db connection is closed when teardown app?
    # db_session.execute("SELECT 1")
    # assert False
    pass


def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr("flaskr.database.init_db", fake_init_db)
    result = runner.invoke(args=["init-db"])
    assert "Initialized" in result.output
    assert Recorder.called


def test_load_test_data_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_load_test_data():
        Recorder.called = True

    monkeypatch.setattr("flaskr.database.load_test_data", fake_load_test_data)
    result = runner.invoke(args=["load-test-data"])
    assert "Loaded some test data" in result.output
    assert Recorder.called
