import pytest

from flaskr.db_service import (
    get_tags_by_post,
    get_posts_by_tag,
    get_top_tags,
    get_tag_id,
    insert_tag,
    get_or_insert_tag,
    attach_tags_with_post,
    count_posts,
    insert_post,
    update_tags_by_post_id,
)


def test_tags_present(app):
    with app.app_context():
        tags = get_tags_by_post(1)

    assert len(tags) == 4
    values = map(lambda t: t.name, tags)

    assert "test" in values
    assert "dhaka" in values
    assert "blog" in values
    assert "python" in values


def test_get_posts_by_tag(app):
    with app.app_context():
        posts = get_posts_by_tag("test")

    assert len(posts) == 3
    # should be fetched in this order, recent first
    assert posts[0].id == 1
    assert posts[1].id == 3
    assert posts[2].id == 5


def test_get_top_tags(app):
    with app.app_context():
        tags = get_top_tags()

    assert_tag(tags, "test", 3)
    assert_tag(tags, "dhaka", 2)
    assert_tag(tags, "blog", 2)
    assert_tag(tags, "python", 2)
    assert_tag(tags, "flask", 1)


def assert_tag(container, name, count):
    for (k, v) in container.items():
        if k == name:
            assert v == count


def test_get_tag_by_id(app):
    with app.app_context():
        tag_id = get_tag_id("python")
        non_existent_tag = get_tag_id("java")
    assert tag_id is not None
    assert non_existent_tag is None


def test_insert_tag(app):
    with app.app_context():
        tag_id_before_insert = get_tag_id("java")
        insert_tag("java")
        tag_id = get_tag_id("java")
    assert tag_id_before_insert is None
    assert tag_id is not None


def test_get_or_insert_tag(app):
    with app.app_context():
        first_id = get_or_insert_tag("python")
        second_id = get_or_insert_tag("java")
    assert first_id is not None
    assert second_id is not None


def test_attach_tags_with_post(app):
    with app.app_context():
        tags_before = get_tags_by_post(10)
        attach_tags_with_post(10, [1, 2, 3])
        tags_after = get_tags_by_post(10)
    assert len(tags_before) == 0
    assert len(tags_after) == 3


def test_insert_post(app):
    with app.app_context():
        current_count = count_posts()
        post_id = insert_post(
            "new post", "new body", "new_file", 1, tags=["java", "python", "scala"]
        )
        count_after = count_posts()
        tags = get_tags_by_post(post_id)

    assert current_count + 1 == count_after
    assert len(tags) == 3


def test_update_tags_by_post_id(app):
    with app.app_context():
        update_tags_by_post_id(1, ["java", "python", "scala", "go", "ruby"])
        tags = get_tags_by_post(1)

    assert len(tags) == 5
