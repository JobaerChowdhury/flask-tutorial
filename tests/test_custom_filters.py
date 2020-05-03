import pytest

from flaskr.custom_filters import md_to_html


def test_markdown_basic():
    md_text = """###This is a markdown text.
simple paragraph

 * list 1
 * list 2
 * list 3
    """

    html = md_to_html(md_text)
    assert "<h3>This is a markdown text.</h3>" in html
    assert "<p>simple paragraph</p>" in html
    assert "<ul>" in html
    assert "<li>list 1</li>" in html
