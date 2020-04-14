import pytest
import json
from flaskr.db import get_db


def test_like(auth, client):
    auth.login()
    response = client.get("/reactions/post/2/like")
    assert response.status_code == 302
    assert "/2/detail" in response.headers["Location"]

    response = client.get("/reactions/post/2/count")
    assert response.status_code == 200
    result = json.loads(response.data)
    assert result["like"] == 1


def test_like_without_login(client):
    response = client.get("/reactions/post/2/like")
    assert response.status_code != 200


def test_like_multiple(auth, client):
    auth.login()
    client.get("/reactions/post/2/like")
    client.get("/reactions/post/2/like")
    client.get("/reactions/post/2/like")

    response = client.get("/reactions/post/2/count")
    assert response.status_code == 200
    result = json.loads(response.data)
    assert result["like"] == 1


def test_unlike(auth, client):
    auth.login()
    response = client.get("/reactions/post/2/unlike")
    assert response.status_code == 302
    assert "/2/detail" in response.headers["Location"]

    response = client.get("/reactions/post/2/count")
    assert response.status_code == 200
    result = json.loads(response.data)
    assert result["unlike"] == 1


def test_unlike_multiple(auth, client):
    auth.login()
    client.get("/reactions/post/2/unlike")
    client.get("/reactions/post/2/unlike")
    client.get("/reactions/post/2/unlike")

    response = client.get("/reactions/post/2/count")
    assert response.status_code == 200
    result = json.loads(response.data)
    assert result["unlike"] == 1


def test_unlike_without_login(client):
    response = client.get("/reactions/post/2/like")
    assert response.status_code != 200


def test_count(client):
    response = client.get("/reactions/post/1/count")
    assert response.status_code == 200
    result = json.loads(response.data)
    assert result["like"] == 3
    assert result["unlike"] == 2


def test_count_zero(client):
    response = client.get("/reactions/post/2/count")
    assert response.status_code == 200
    result = json.loads(response.data)
    assert result["like"] == 0
    assert result["unlike"] == 0
