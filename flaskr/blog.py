import os
from flask import (
    Blueprint,
    current_app,
    send_from_directory,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for,
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from flaskr.db import get_db
from flaskr.auth import login_required
from flaskr.reaction import get_reactions

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

bp = Blueprint("blog", __name__)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route("/")
def index():
    db = get_db()
    posts = db.execute(
        "SELECT p.id, title, body, created, author_id, username"
        " FROM post p JOIN user u ON p.author_id = u.id"
        " ORDER BY created DESC"
    ).fetchall()

    return render_template("blog/index.html", posts=posts)


@bp.route("/<int:post_id>/detail")
def detail(post_id):
    post = get_post(post_id, check_author=False)
    reactions = get_reactions(post_id)
    return render_template("blog/detail.html", post=post, reactions=reactions)


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        # check if the post request has the file part
        filename = None
        if "file" in request.files:
            file = request.files["file"]
            if file.filename == "":
                pass
            elif file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # TODO Will it raise excpetion here?
                file.save(os.path.join(current_app.config["UPLOAD_DIR"], filename))
            else:
                error = "File is not allowed."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO post (title, body, image_path, author_id)"
                " VALUES (?, ?, ?, ?)",
                (title, body, filename, g.user["id"]),
            )
            db.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/create.html")


@bp.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(current_app.config["UPLOAD_DIR"], filename)


def get_post(id, check_author=True):
    post = (
        get_db()
        .execute(
            "SELECT p.id, title, body, image_path, created, author_id, username"
            " FROM post p JOIN user u ON p.author_id = u.id"
            " WHERE p.id = ?",
            (id,),
        )
        .fetchone()
    )

    if post is None:
        abort(404, "Post id {0} doesn't exist".format(id))

    if check_author and post["author_id"] != g.user["id"]:
        abort(403)

    return post


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    post = get_post(id)
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        # check if the post request has the file part
        filename = None
        if "file" in request.files:
            file = request.files["file"]
            if file.filename == "":
                pass
            elif file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # TODO Will it raise excpetion here?
                file.save(os.path.join(current_app.config["UPLOAD_DIR"], filename))
            else:
                error = "File is not allowed."
        print(filename)

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE post SET title = ?, body = ?" " WHERE id = ?", (title, body, id)
            )
            if filename:
                if post["image_path"] is None or filename != post["image_path"]:
                    db.execute(
                        "UPDATE post SET image_path = ?" " WHERE id = ?", (filename, id)
                    )
            db.commit()
            return redirect(url_for("blog.index"))
    return render_template("blog/update.html", post=post)


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute("DELETE FROM post WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("blog.index"))
