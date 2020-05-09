from collections import OrderedDict
from sqlalchemy import func, desc
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.database import db
from flaskr.models import Tag, Post, User, Reaction, post_tag, Comment
from flaskr.db_util import get_or_create


def get_user_by_id(user_id):
    return User.query.get(user_id)


def get_user_by_username(username):
    return User.query.filter_by(username=username).first()


def insert_user(username, password):
    user = User(username=username, password=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()


def insert_or_update_reaction(name, user_id, post_id):
    reaction = (
        db.session.query(Reaction).filter_by(entity_id=post_id, user_id=user_id).first()
    )

    if reaction is None:
        db.session.add(Reaction(name=name, entity_id=post_id, user_id=user_id))
    else:
        reaction.name = name
    db.session.commit()


def get_reactions_by_entityid(entity_id, reactions=[]):
    results = (
        db.session.query(Reaction.name, func.count(Reaction.name))
        .filter_by(entity_id=entity_id)
        .group_by(Reaction.name)
        .all()
    )

    resp = dict()
    for (name, count) in results:
        resp[name] = count

    for r in reactions:
        if r not in resp:
            resp[r] = 0

    return resp


def get_posts(limit, offset):
    posts = (
        db.session.query(Post)
        .order_by(desc(Post.created))
        .slice(offset, offset + limit)
        .all()
    )
    return posts


def count_posts():
    return db.session.query(func.count(Post.id)).scalar()


def insert_post(title, body, filename, user_id, tags=[]):
    post = Post(title=title, body=body, image_path=filename, author_id=user_id)
    db.session.add(post)

    if len(tags) > 0:
        db_tags = get_persistent_tags(tags)
        post.tags = db_tags

    db.session.commit()
    return post.id


def get_persistent_tags(tagnames):
    """Returns a set of database tag objects matching the tagnames parameter.
    If a tag is not present in db for the given tagname then it will be created.

    Returns a list of Tag objects.
    """
    tags = []
    for tagname in tagnames:
        tag = get_or_create(db.session, Tag, name=tagname)
        tags.append(tag)
    return tags


def get_post_by_id(id):
    return Post.query.get(id)


def get_tag_by_name(name):
    return Tag.query.filter_by(name=name).first()


def insert_tag(name):
    db.session.add(Tag(name=name))
    db.session.commit()


def attach_tags_with_post(post_id, tag_ids):
    post = Post.query.get(post_id)
    for tag_id in tag_ids:
        tag = Tag.query.get(tag_id)
        if tag is not None:
            post.tags.append(tag)
    db.session.add(post)
    db.session.commit()


def update_post(title, body, id):
    post = Post.query.get(id)
    post.title = title
    post.body = body
    db.session.commit()


def update_tags_by_post_id(post_id, tags):
    post = db.session.query(Post).get(post_id)
    post.tags = []

    db_tags = get_persistent_tags(tags)
    post.tags = db_tags
    db.session.commit()


def update_image_by_post_id(filename, id):
    post = Post.query.get(id)
    post.image_path = filename
    db.session.commit()


def delete_post_by_id(id):
    db.session.query(Post).filter(Post.id == id).delete()
    db.session.commit()


def get_tags_by_post(id):
    post = Post.query.get(id)
    return post.tags


def count_posts_by_tag(tagname):
    tag = get_tag_by_name(tagname)
    if tag is not None:
        return len(tag.posts)
    else:
        return 0


def get_posts_by_tag(tagname, limit=5, offset=0):
    # given a tag, return the posts, recent first, with limit and offset
    return (
        Post.query.filter(Post.tags.any(name=tagname))
        .order_by(desc(Post.created))
        .slice(offset, (offset + limit + 1))
        .all()
    )


def get_top_tags(limit=10):
    # return the top tags, ordered by number of posts tagged with
    subq = (
        db.session.query(
            post_tag.c.tag_id, func.count(post_tag.c.post_id).label("total")
        )
        .group_by(post_tag.c.tag_id)
        .subquery()
    )

    rows = (
        db.session.query(Tag, subq.c.total)
        .join(subq, Tag.id == subq.c.tag_id)
        .order_by(desc(subq.c.total))
        .limit(limit)
        .all()
    )

    tags = OrderedDict()

    for (tag, total) in rows:
        tags[tag.name] = total

    return tags


def count_comments_by_post(post_id):
    return db.session.query(func.count(Comment.id)).filter_by(post_id=post_id).scalar()


def get_comments_by_post(post_id):
    return (
        db.session.query(Comment)
        .filter_by(post_id=post_id)
        .order_by(desc(Comment.created))
        .all()
    )


def insert_comment(post_id, user_id, content):
    comment = Comment(post_id=post_id, author_id=user_id, content=content)
    db.session.add(comment)
    db.session.commit()
    return comment.id


def get_comment_by_id(comment_id):
    return Comment.query.get(comment_id)


def update_comment(comment_id, new_content):
    comment = Comment.query.get(comment_id)
    if comment:
        comment.content = new_content
        db.session.commit()


def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)
    db.session.delete(comment)
    db.session.commit()
