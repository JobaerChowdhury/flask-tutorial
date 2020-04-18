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


def insert_post(title, body, filename, user_id):
    db = get_db()
    db.execute(
        "INSERT INTO post (title, body, image_path, author_id)" " VALUES (?, ?, ?, ?)",
        (title, body, filename, user_id),
    )
    db.commit()


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


def update_post(title, body, id):
    db = get_db()
    db.execute("UPDATE post SET title = ?, body = ?" " WHERE id = ?", (title, body, id))
    db.commit()


def update_image_by_post_id(filename, id):
    db = get_db()
    db.execute("UPDATE post SET image_path = ?" " WHERE id = ?", (filename, id))
    db.commit()


def delete_post_by_id(id):
    db = get_db()
    db.execute("DELETE FROM post WHERE id = ?", (id,))
    db.commit()
