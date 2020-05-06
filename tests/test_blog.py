import os
import io
import pytest

from flaskr.database import db
from flaskr.models import Post, Tag, User
from sqlalchemy import func


image_file_path = os.path.join(os.path.dirname(__file__), "sample_image.png")
with open(image_file_path, "rb") as f:
    _data_image = f.read()


def test_index(client, auth):
    response = client.get("/")
    assert b"Log In" in response.data
    assert b"Register" in response.data

    auth.login()
    response = client.get("/")
    assert response.status_code == 200
    assert b"Log Out" in response.data
    assert b"test title" in response.data
    assert b"by test on 2020-01-01" in response.data
    assert b'href="/1/update"' in response.data
    assert b'href="/1/detail"' in response.data
    assert b'href="/?page=0"' in response.data
    assert b'href="/?page=1"' in response.data
    assert b'href="/?page=2"' in response.data


def test_index_tags(client, auth):
    response = client.get("/")
    assert b"Most frequent tags" in response.data
    assert b'href="/tag/test"' in response.data
    assert b'href="/tag/dhaka"' in response.data
    assert b'href="/tag/blog"' in response.data


def test_tag_page(client):
    response = client.get("/tag/test")
    assert response.status_code == 200
    assert b'href="/1/detail"' in response.data
    assert b'href="/3/detail"' in response.data
    assert b'href="/5/detail"' in response.data


def test_tag_page_no_post(client):
    response = client.get("/tag/tagnotpresent")
    assert response.status_code == 200
    assert b"No posts found" in response.data


def test_detail_with_image(client, auth):
    # test 404, and 200 with both logged in and out
    assert client.get("/393/detail").status_code == 404

    resp = client.get("/1/detail")
    assert resp.status_code == 200
    assert b"test title" in resp.data
    assert b"test body without image" in resp.data
    assert b'src="/uploads/test_image.jpg"' in resp.data

    auth.login()
    resp = client.get("/1/detail")
    assert resp.status_code == 200


def test_detail_without_image(client, auth):
    resp = client.get("/2/detail")
    assert resp.status_code == 200
    print(resp.data)
    assert b"post without image" in resp.data
    assert b'src="/uploads"' not in resp.data


def test_detail_reactions(client, auth):
    resp = client.get("/2/detail")
    assert resp.status_code == 200
    print(resp.data)
    assert b'href="/reactions/post/2/like"' in resp.data
    assert b'href="/reactions/post/2/unlike"' in resp.data


def test_detail_tag_present(client, auth):
    resp = client.get("/1/detail")
    assert resp.status_code == 200
    assert b'href="/tag/dhaka"' in resp.data
    assert b'href="/tag/test"' in resp.data
    assert b'href="/tag/blog"' in resp.data


def test_detail_reaction_count(client, auth):
    resp = client.get("/1/detail")
    assert resp.status_code == 200
    assert b'Liked by <span class="blue">3' in resp.data
    assert b'unliked by <span class="red">2' in resp.data


@pytest.mark.parametrize("path", ("/create", "/1/update", "/1/delete",))
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers["Location"] == "http://localhost/auth/login"


def test_author_required(app, client, auth):
    # change the post author to another user
    with app.app_context():
        post = Post.query.get(1)
        post.author_id = 2
        db.session.commit()

    auth.login()
    # current user can't modify other user's post
    assert client.post("/1/update").status_code == 403
    assert client.post("/1/delete").status_code == 403
    # current user doesn't see edit link
    assert b'href="/1/update"' not in client.get("/").data


@pytest.mark.parametrize("path", ("/20/update", "/20/delete",))
def test_exists_required(client, auth, path):
    auth.login()
    assert client.post(path).status_code == 404


def test_create(client, auth, app):
    with app.app_context():
        current_count = db.session.query(func.count(Post.id)).scalar()

    auth.login()
    assert client.get("/create").status_code == 200
    client.post("/create", data={"title": "created", "body": ""})

    with app.app_context():
        count = db.session.query(func.count(Post.id)).scalar()
        assert count == current_count + 1


def test_create_with_tags(client, auth, app):
    with app.app_context():
        post_count_before = db.session.query(func.count(Post.id)).scalar()
        tag_count_before = db.session.query(func.count(Tag.id)).scalar()

    auth.login()
    assert client.get("/create").status_code == 200
    client.post(
        "/create", data={"title": "created", "body": "", "tags": "java scala python"}
    )

    with app.app_context():
        post_count = db.session.query(func.count(Post.id)).scalar()
        tag_count = db.session.query(func.count(Tag.id)).scalar()

    assert post_count == post_count_before + 1
    # count should increase by two, since 'python' is an existing tag
    assert tag_count == tag_count_before + 2


def test_create_with_image(client, auth, app):
    with app.app_context():
        current_count = db.session.query(func.count(Post.id)).scalar()

    auth.login()
    create_with_image(client, "article_image.png")

    assert client.get("/create").status_code == 200
    with app.app_context():
        count = db.session.query(func.count(Post.id)).scalar()

    assert count == current_count + 1


def test_create_invalid_image(client, auth, app):
    auth.login()
    response = create_with_image(client, "article_image.tmp")
    assert b"File is not allowed." in response.data


def create_with_image(client, filename):
    data = {
        "title": "created",
        "body": "some body",
        "file": (io.BytesIO(_data_image), filename),
    }
    return client.post("/create", data=data, content_type="multipart/form-data")


def test_upload_path_ok(client, auth, app):
    auth.login()
    filename = "test_image.png"
    create_with_image(client, filename)

    image_serve_path = "/uploads/%s" % filename
    assert client.get(image_serve_path).status_code == 200


def test_upload_path_not_found(client):
    image_serve_path = "/uploads/non-existent.png"
    assert client.get(image_serve_path).status_code == 404


def test_update(client, auth, app):
    auth.login()
    assert client.get("/1/update").status_code == 200
    client.post("/1/update", data={"title": "updated", "body": ""})

    with app.app_context():
        post = Post.query.get(1)
        assert post.title == "updated"
        assert post.image_path == "test_image.jpg"  # should not be updated


def test_update_with_tags(client, auth, app):
    auth.login()
    assert client.get("/1/update").status_code == 200
    client.post(
        "/1/update",
        data={"title": "updated", "body": "", "tags": "java python sql go scala"},
    )

    with app.app_context():
        post = Post.query.get(1)
        assert post.title == "updated"
        tag_count = len(post.tags)
    assert tag_count == 5


def test_update_with_image(client, auth, app):
    auth.login()
    assert client.get("/1/update").status_code == 200
    data = {
        "title": "updated",
        "body": "some body",
        "file": (io.BytesIO(_data_image), "new_image.png"),
    }
    client.post("/1/update", data=data, content_type="multipart/form-data")

    with app.app_context():
        post = Post.query.get(1)
        assert post.title == "updated"
        assert post.image_path == "new_image.png"  # should be updated


def test_update_post_adding_image(client, auth, app):
    auth.login()
    assert client.get("/2/update").status_code == 200
    data = {
        "title": "updated",
        "body": "some body",
        "file": (io.BytesIO(_data_image), "new_image.png"),
    }
    client.post("/2/update", data=data, content_type="multipart/form-data")

    with app.app_context():
        post = Post.query.get(2)
        assert post.title == "updated"
        assert post.image_path == "new_image.png"  # should be updated


@pytest.mark.parametrize("path", ("/create", "/1/update",))
def test_create_update_validate(client, auth, path):
    auth.login()
    response = client.post(path, data={"title": "", "body": ""})
    assert b"Title is required." in response.data


def test_delete(client, auth, app):
    auth.login()
    response = client.post("/1/delete")
    assert response.headers["Location"] == "http://localhost/"

    with app.app_context():
        post = Post.query.get(1)
        assert post is None
