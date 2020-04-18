import os
import math
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

from flaskr.auth import login_required
from flaskr.reaction import REACTIONS
from flaskr.db_service import (
    get_reactions_by_entityid,
    get_posts,
    count_posts,
    insert_post,
    get_post_by_id,
    update_post,
    update_image_by_post_id,
    delete_post_by_id,
)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
PAGE_SIZE = 5

bp = Blueprint("blog", __name__)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route("/")
def index():
    page = _get_page(request)
    limit = PAGE_SIZE
    offset = PAGE_SIZE * page

    posts = get_posts(limit, offset)
    size = count_posts()

    (q, r) = divmod(size, PAGE_SIZE)
    if r == 0:
        pages = q
    else:
        pages = q + 1

    return render_template("blog/index.html", posts=posts, pages=pages)


def _get_page(request):
    if request.args.get("page"):
        try:
            return int(request.args.get("page"))
        except ValueError:
            return 0
    return 0


@bp.route("/<int:post_id>/detail")
def detail(post_id):
    post = get_post(post_id, check_author=False)
    reactions = get_reactions_by_entityid(post_id, reactions=REACTIONS)
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
            insert_post(title, body, filename, g.user["id"])
            return redirect(url_for("blog.index"))

    return render_template("blog/create.html")


@bp.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(current_app.config["UPLOAD_DIR"], filename)


def get_post(id, check_author=True):
    post = get_post_by_id(id)

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
            update_post(title, body, id)
            if filename:
                if post["image_path"] is None or filename != post["image_path"]:
                    update_image_by_post_id(filename, id)
            return redirect(url_for("blog.index"))
    return render_template("blog/update.html", post=post)


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    get_post(id)
    delete_post_by_id(id)
    return redirect(url_for("blog.index"))
