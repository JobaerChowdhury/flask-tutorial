import pytest

from flaskr.db_service import (
    get_tags_by_post,
    get_tag_by_name,
    get_posts_by_tag,
    get_top_tags,
    insert_tag,
    attach_tags_with_post,
    get_persistent_tags,
    count_posts,
    insert_post,
    update_tags_by_post_id,
    count_posts_by_tag,
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


def test_get_persistent_tags(app):
    tagnames = ["python", "test", "dhaka", "blog", "java", "scala"]  # 4 existing, 2 new
    with app.app_context():
        tags = get_persistent_tags(tagnames)
        for tag in tags:
            assert tag is not None
            assert tag.id > 0


def test_insert_tag(app):
    with app.app_context():
        before = get_tag_by_name("java")
        insert_tag("java")
        after = get_tag_by_name("java")
    assert before is None
    assert after is not None


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


def test_tag_count(app):
    with app.app_context():
        tag_count = count_posts_by_tag("test")
    assert tag_count == 3
