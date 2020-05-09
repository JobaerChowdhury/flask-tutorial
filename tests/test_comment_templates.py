import pytest

from flaskr.database import db
from flaskr.models import Post, Tag, User
from sqlalchemy import func


def test_comment_form_not_present(client):
    response = client.get("/1/detail")
    assert response.status_code == 200

    assert b"<h4>You must login to post comment</h4>" in response.data
    assert b'form id="commentForm"' not in response.data
    assert b'action="/1/comment"' not in response.data


def test_comment_form_present(client, auth):
    auth.login()
    response = client.get("/1/detail")
    assert response.status_code == 200

    assert b"<h4>You must login to post comment</h4>" not in response.data
    assert b'form id="commentForm"' in response.data
    assert b'action="/1/comment"' in response.data


def test_comment(client, auth):
    auth.login()
    response = client.get("/1/detail")
    assert response.status_code == 200
    assert b'form id="commentForm"' in response.data

    post_resp = client.post(
        "/1/comment", data={"comment-body": "this is a test comment"}
    )
    assert post_resp.status_code == 302
    assert post_resp.headers["Location"] == "http://localhost/1/detail"


def test_comment_without_login(client):
    post_resp = client.post(
        "/1/comment", data={"comment-body": "this is a test comment"}
    )
    assert post_resp.status_code == 302
    assert post_resp.headers["Location"] == "http://localhost/auth/login"
