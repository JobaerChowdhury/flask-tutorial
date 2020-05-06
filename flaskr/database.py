import os
import click

from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def init_db():
    import flaskr.models

    db.drop_all()
    db.create_all()


@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("Initialized the database")


def load_test_data():
    from flaskr import testdata

    testdata.load_test_data()


@click.command("load-test-data")
@with_appcontext
def load_test_data_command():
    """Loads some sample data into the database."""
    load_test_data()
    click.echo("Loaded some test data")


def init_app(app):
    app.cli.add_command(init_db_command)
    app.cli.add_command(load_test_data_command)
