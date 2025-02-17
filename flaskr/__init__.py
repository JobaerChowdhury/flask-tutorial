import os

from flask import Flask


IMAGES_DIR = "images"


def create_app(test_config=None):
    configure_logging()
    # create and cofigure the app
    app = Flask(__name__, instance_relative_config=True)
    DATABASE = os.path.join(app.instance_path, "flaskr.sqlite")
    app.config.from_mapping(
        SECRET_KEY="dev",
        UPLOAD_DIR=(os.path.join(app.instance_path, IMAGES_DIR)),
        SQLALCHEMY_DATABASE_URI="sqlite:///" + DATABASE,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test_config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # ensure the upload folder exists
    try:
        os.makedirs(app.config["UPLOAD_DIR"])
    except OSError:
        pass

    # A simple page that says hello
    @app.route("/hello")
    def hello():
        return "Hello, World!"

    from . import database

    database.db.init_app(app)
    database.init_app(app)

    from . import auth
    from . import blog
    from . import reaction
    from . import feed
    from . import custom_filters

    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.register_blueprint(reaction.bp)
    app.register_blueprint(feed.bp)
    app.add_url_rule("/", "index")
    custom_filters.init_app(app)

    return app


def configure_logging():
    from logging.config import dictConfig

    dictConfig(
        {
            "version": 1,
            "formatters": {
                "default": {
                    "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
                }
            },
            "handlers": {
                "wsgi": {
                    "class": "logging.StreamHandler",
                    "stream": "ext://flask.logging.wsgi_errors_stream",
                    "formatter": "default",
                }
            },
            "root": {"level": "INFO", "handlers": ["wsgi"]},
        }
    )
