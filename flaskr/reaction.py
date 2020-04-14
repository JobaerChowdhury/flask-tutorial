# Blueprint for like/unlike.
from flask import Blueprint, g, current_app, request, url_for, redirect

from flaskr.db import get_db
from flaskr.auth import login_required

bp = Blueprint("reaction", __name__)

# TODO Maybe convert to Enum
REACTIONS = ("like", "unlike")


@bp.route("/reactions/post/<int:post_id>/like")
@login_required
def like_post(post_id):
    # like a post
    user_id = g.user["id"]
    _insert_or_update(REACTIONS[0], user_id, post_id)
    return redirect(url_for("blog.detail", post_id=post_id))


@bp.route("/reactions/post/<int:post_id>/unlike")
@login_required
def unlike_post(post_id):
    # unlike a post
    user_id = g.user["id"]
    _insert_or_update(REACTIONS[1], user_id, post_id)

    return redirect(url_for("blog.detail", post_id=post_id))


def _insert_or_update(name, user_id, post_id):
    db = get_db()
    existing = db.execute(
        "SELECT name FROM reaction WHERE entity_id = ? and user_id = ?",
        (post_id, user_id),
    ).fetchone()

    if existing is None:
        db.execute(
            "INSERT INTO reaction (name, user_id, entity_id) VALUES (?, ?, ?)",
            (name, user_id, post_id),
        )
    else:
        db.execute(
            "UPDATE reaction SET name = ? WHERE user_id = ? AND entity_id = ?",
            (name, user_id, post_id),
        )
    db.commit()


def get_reactions(post_id):
    db = get_db()
    results = db.execute(
        "SELECT name, COUNT(name) AS count FROM reaction WHERE entity_id = ? GROUP BY name",
        (post_id,),
    ).fetchall()
    resp = dict()
    for row in results:
        k = row["name"]
        v = row["count"]
        resp[k] = v

    for r in REACTIONS:
        if r not in resp:
            resp[r] = 0

    return resp


@bp.route("/reactions/post/<int:post_id>/count")
def count_post(post_id):
    # return a dict with the count of each reaction for a post
    return get_reactions(post_id)
