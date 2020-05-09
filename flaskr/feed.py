from flask import request, Blueprint, url_for, Response
from feedgen.feed import FeedGenerator
from flaskr.db_service import get_posts
from flaskr.custom_filters import md_to_html

from datetime import datetime
from datetime import timezone

bp = Blueprint("feed", __name__)


@bp.route("/feeds/")
def feeds():
    feed = _prepare_feed()
    atomfeed = feed.atom_str(pretty=True)
    return Response(atomfeed, mimetype="application/atom+xml")


def _prepare_feed():
    fg = FeedGenerator()
    fg.id(str(request.url))
    fg.title("Latest stories from flaskr blog")
    fg.link(href=str(request.url), rel="self")
    fg.link(href=str(request.url_root), rel="alternate")
    fg.language("en")

    posts = get_posts(limit=10, offset=0)
    posts.reverse()  # the last one added as entry is the latest one

    for post in posts:
        fe = fg.add_entry()
        fe.id(str(post.id))
        fe.link(href=url_for("blog.detail", post_id=post.id))
        fe.title(post.title)
        fe.summary(md_to_html(post.body))
        fe.author(name=post.author.username)
        fe.updated(updated=attach_timezone(post.created))
        fe.published(published=attach_timezone(post.created))

    return fg


def attach_timezone(dt):
    return datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, tzinfo=timezone.utc)
