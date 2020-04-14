import os

from flask import Flask


IMAGES_DIR = "images"


def create_app(test_config=None):
    # create and cofigure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        UPLOAD_DIR=(os.path.join(app.instance_path, IMAGES_DIR)),
        DATABASE=(os.path.join(app.instance_path, "flaskr.sqlite")),
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

    from . import db

    db.init_app(app)

    from . import auth
    from . import blog
    from . import reaction

    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.register_blueprint(reaction.bp)
    app.add_url_rule("/", "index")

    return app
