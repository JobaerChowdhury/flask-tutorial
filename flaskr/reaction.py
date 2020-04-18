# Blueprint for like/unlike.
from flask import Blueprint, g, current_app, request, url_for, redirect

from flaskr.auth import login_required
from flaskr.db_service import insert_or_update_reaction, get_reactions_by_entityid

bp = Blueprint("reaction", __name__)

# TODO Maybe convert to Enum
REACTIONS = ("like", "unlike")


@bp.route("/reactions/post/<int:post_id>/like")
@login_required
def like_post(post_id):
    # like a post
    user_id = g.user["id"]
    insert_or_update_reaction(REACTIONS[0], user_id, post_id)
    return redirect(url_for("blog.detail", post_id=post_id))


@bp.route("/reactions/post/<int:post_id>/unlike")
@login_required
def unlike_post(post_id):
    # unlike a post
    user_id = g.user["id"]
    insert_or_update_reaction(REACTIONS[1], user_id, post_id)

    return redirect(url_for("blog.detail", post_id=post_id))


@bp.route("/reactions/post/<int:post_id>/count")
def count_post(post_id):
    # return a dict with the count of each reaction for a post
    return get_reactions_by_entityid(post_id, reactions=REACTIONS)
