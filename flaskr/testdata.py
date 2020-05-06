from datetime import datetime, timezone

from flaskr.models import User, Post, Tag, Reaction
from flaskr.database import db


def load_test_data():
    print("Creating some test data ... ")
    load_users()
    load_posts()
    load_tags()
    load_reactions()


def load_users():
    test_user = User(
        username="test",
        password="pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f",
    )
    admin_user = User(
        username="admin",
        password="pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f",
    )
    other_user = User(
        username="other",
        password="pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79",
    )
    db.session.add(test_user)
    db.session.add(admin_user)
    db.session.add(other_user)
    db.session.commit()


def load_posts():
    test_user = User.query.filter(User.username == "test").first()
    post1 = Post(
        title="test title",
        body="test body without image",
        image_path="test_image.jpg",
        author_id=test_user.id,
        created=datetime(2020, 1, 1, 15, 17, tzinfo=timezone.utc),
    )
    db.session.add(post1)

    for i in range(10):
        db.session.add(
            Post(
                title="post without image - " + str(i),
                body="test body without image",
                author_id=test_user.id,
                created=datetime(2019, 5, 18, (15 - i), 17, tzinfo=timezone.utc),
            )
        )
    db.session.commit()


def load_tags():
    db.session.add(Tag(name="test"))
    db.session.add(Tag(name="dhaka"))
    db.session.add(Tag(name="blog"))
    db.session.add(Tag(name="new"))
    db.session.add(Tag(name="python"))
    db.session.add(Tag(name="flask"))
    db.session.commit()

    test = Tag.query.filter(Tag.name == "test").first()
    dhaka = Tag.query.filter(Tag.name == "dhaka").first()
    blog = Tag.query.filter(Tag.name == "blog").first()
    python = Tag.query.filter(Tag.name == "python").first()
    flask = Tag.query.filter(Tag.name == "flask").first()

    post1 = Post.query.filter(Post.id == 1).first()
    post2 = Post.query.filter(Post.id == 2).first()
    post3 = Post.query.filter(Post.id == 3).first()
    post4 = Post.query.filter(Post.id == 4).first()
    post5 = Post.query.filter(Post.id == 5).first()
    post6 = Post.query.filter(Post.id == 6).first()

    test.posts.append(post1)
    test.posts.append(post3)
    test.posts.append(post5)

    dhaka.posts.append(post1)
    dhaka.posts.append(post2)

    blog.posts.append(post1)
    blog.posts.append(post4)

    python.posts.append(post1)
    python.posts.append(post2)

    flask.posts.append(post6)

    db.session.commit()


def load_reactions():
    db.session.add(Reaction(name="like", user_id=1, entity_id=1))
    db.session.add(Reaction(name="like", user_id=2, entity_id=1))
    db.session.add(Reaction(name="like", user_id=3, entity_id=1))
    db.session.add(Reaction(name="unlike", user_id=1, entity_id=1))
    db.session.add(Reaction(name="unlike", user_id=2, entity_id=1))
    db.session.commit()
