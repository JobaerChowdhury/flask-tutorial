from sqlalchemy.sql.functions import now

from flaskr.database import db


post_tag = db.Table(
    "post_tag",
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id")),
    db.Column("post_id", db.Integer, db.ForeignKey("post.id")),
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(200), nullable=False)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    title = db.Column(db.String(500), nullable=False)
    body = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(200), nullable=True)
    created = db.Column(db.DateTime(timezone=True), server_default=now())
    author = db.relationship("User")
    tags = db.relationship(
        "Tag", secondary=post_tag, backref=db.backref("posts", lazy=True)
    )


class Reaction(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    entity_id = db.Column(db.Integer, db.ForeignKey("post.id"))
    created = db.Column(db.DateTime(timezone=True), server_default=now())
    user = db.relationship("User")


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), unique=True)
