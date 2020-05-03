import markdown


def init_app(app):
    app.add_template_filter(md_to_html, name="from_markdown")


def md_to_html(text):
    return markdown.markdown(text)
