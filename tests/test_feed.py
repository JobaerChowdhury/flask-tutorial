import pytest

from flaskr.database import db


def test_feeds_basic(client, auth):
    response = client.get("/feeds/")

    assert response.status_code == 200
    assert response.content_type == "application/atom+xml; charset=utf-8"

    assert b"<title>Latest stories from flaskr blog</title>" in response.data
    assert b'href="/1/detail"' in response.data
    assert b"<title>test title</title>" in response.data
    assert b"<name>test</name>" in response.data
    assert b"test body without image" in response.data
