from collections import OrderedDict

from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db


def get_user_by_id(user_id):
    return get_db().execute("SELECT * FROM user where id = ?", (user_id,)).fetchone()


def get_user_by_username(username):
    return (
        get_db()
        .execute("SELECT * FROM user WHERE username = ?", (username,))
        .fetchone()
    )


def insert_user(username, password):
    db = get_db()
    db.execute(
        "INSERT INTO user (username, password) VALUES (?, ?)",
        (username, generate_password_hash(password)),
    )
    db.commit()


def insert_or_update_reaction(name, user_id, post_id):
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


def get_reactions_by_entityid(etity_id, reactions=[]):
    db = get_db()
    results = db.execute(
        "SELECT name, COUNT(name) AS count FROM reaction WHERE entity_id = ? GROUP BY name",
        (etity_id,),
    ).fetchall()
    resp = dict()
    for row in results:
        k = row["name"]
        v = row["count"]
        resp[k] = v

    for r in reactions:
        if r not in resp:
            resp[r] = 0

    return resp


def get_posts(limit, offset):
    db = get_db()
    posts = db.execute(
        "SELECT p.id, title, body, created, author_id, username"
        " FROM post p JOIN user u ON p.author_id = u.id"
        " ORDER BY created DESC"
        " LIMIT ? OFFSET ?",
        (limit, offset),
    ).fetchall()
    return posts


def count_posts():
    db = get_db()
    total = db.execute("SELECT COUNT(id) from post").fetchone()[0]
    return total


def insert_post(title, body, filename, user_id, tags=[]):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO post (title, body, image_path, author_id) VALUES (?, ?, ?, ?)",
        (title, body, filename, user_id),
    )
    post_id = cursor.lastrowid
    db.commit()

    tag_ids = get_ids_or_insret_tags(tags)
    attach_tags_with_post(post_id, tag_ids)

    return post_id


def get_ids_or_insret_tags(tags):
    tag_ids = []
    for tag in tags:
        tag_id = get_or_insert_tag(tag)
        if tag_id is not None:
            tag_ids.append(tag_id)
    return tag_ids


def get_post_by_id(id):
    return (
        get_db()
        .execute(
            "SELECT p.id, title, body, image_path, created, author_id, username"
            " FROM post p JOIN user u ON p.author_id = u.id"
            " WHERE p.id = ?",
            (id,),
        )
        .fetchone()
    )


def get_tag_id(name):
    db = get_db()
    tag_id = db.execute("SELECT id FROM tag  WHERE name = ?", (name,)).fetchone()
    if tag_id is not None:
        return tag_id["id"]
    else:
        return None


def insert_tag(name):
    db = get_db()
    db.execute("INSERT INTO tag (name) VALUES (?)", (name,))
    db.commit()


def get_or_insert_tag(name):
    tag_id = get_tag_id(name)
    if tag_id is not None:
        return tag_id

    insert_tag(name)
    return get_tag_id(name)


def attach_tags_with_post(post_id, tag_ids):
    db = get_db()
    for tag_id in tag_ids:
        db.execute(
            "INSERT INTO post_tag (tag_id, entity_id) values (?, ?) ", (tag_id, post_id)
        )
    db.commit()


def update_post(title, body, id):
    db = get_db()
    db.execute("UPDATE post SET title = ?, body = ?" " WHERE id = ?", (title, body, id))
    db.commit()


def update_tags_by_post_id(post_id, tags):
    db = get_db()
    db.execute("DELETE FROM post_tag WHERE entity_id = ?", (post_id,))
    db.commit()
    tag_ids = get_ids_or_insret_tags(tags)
    attach_tags_with_post(post_id, tag_ids)


def update_image_by_post_id(filename, id):
    db = get_db()
    db.execute("UPDATE post SET image_path = ?" " WHERE id = ?", (filename, id))
    db.commit()


def delete_post_by_id(id):
    db = get_db()
    db.execute("DELETE FROM post WHERE id = ?", (id,))
    db.commit()


def get_tags_by_post(id):
    # return a list of tags
    db = get_db()
    tag_rows = db.execute(
        "SELECT t.id, name FROM tag t JOIN post_tag pt ON t.id = pt.tag_id WHERE pt.entity_id = ?",
        (id,),
    ).fetchall()
    tags = []
    for r in tag_rows:
        tags.append({"id": r["id"], "name": r["name"]})
    return tags


def count_posts_by_tag(tagname):
    db = get_db()
    total = db.execute(
        "SELECT COUNT(p.id)"
        " FROM post p JOIN user u ON p.author_id = u.id"
        " WHERE p.id IN (SELECT pt.entity_id FROM tag t JOIN post_tag pt ON t.id = pt.tag_id WHERE t.name = ?)",
        (tagname,),
    ).fetchone()[0]
    return total


def get_posts_by_tag(tagname, limit=5, offset=0):
    # given a tag, return the posts, recent first, with limit and offset
    db = get_db()
    posts = db.execute(
        "SELECT p.id, title, body, created, author_id, username"
        " FROM post p JOIN user u ON p.author_id = u.id"
        " WHERE p.id IN (SELECT pt.entity_id FROM tag t JOIN post_tag pt ON t.id = pt.tag_id WHERE t.name = ?)"
        " ORDER BY created DESC"
        " LIMIT ? OFFSET ?",
        (tagname, limit, offset),
    ).fetchall()
    return posts


def get_top_tags(limit=10):
    # return the top tags, ordered by number of posts tagged with
    db = get_db()
    tags = OrderedDict()
    result = db.execute(
        "SELECT t.name, tg.total"
        " FROM tag t JOIN"
        "  (SELECT tag_id, count(entity_id) AS total"
        "    FROM post_tag"
        " GROUP BY tag_id) tg"
        " ON t.id = tg.tag_id"
        " ORDER BY tg.total DESC"
        " limit ?",
        (limit,),
    ).fetchall()

    for row in result:
        tags[row["name"]] = row["total"]

    return tags
