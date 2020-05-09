import pytest

from flaskr.db_service import (
    insert_comment,
    get_comments_by_post,
    update_comment,
    delete_comment,
    count_comments_by_post,
    get_comment_by_id,
)


def test_insert_comment(app):
    with app.app_context():
        count_before = count_comments_by_post(1)
        comment_id = insert_comment(
            post_id=1, user_id=1, content="this is a test comment"
        )
        count_after = count_comments_by_post(1)
    assert comment_id > 0
    assert count_after == count_before + 1


def test_update_comment(app):
    with app.app_context():
        comment_id = insert_comment(
            post_id=1, user_id=1, content="this is a test comment"
        )
        assert comment_id > 0
        comment = get_comment_by_id(comment_id)
        assert comment.content == "this is a test comment"
        update_comment(comment_id, "updated body of comment")
        comment = get_comment_by_id(comment_id)
        assert comment.content == "updated body of comment"


def test_delete_comment(app):
    with app.app_context():
        comment_id = insert_comment(
            post_id=1, user_id=1, content="this is a test comment"
        )
        assert comment_id > 0
        delete_comment(comment_id)
        comment = get_comment_by_id(comment_id)
        assert comment is None


def test_get_comments_by_post(app):
    with app.app_context():
        comments = get_comments_by_post(1)
        assert len(comments) == 10
        assert comments[0].id == 1  # Most recent one should be the first
