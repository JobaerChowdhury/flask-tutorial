import markdown


def init_app(app):
    app.add_template_filter(md_to_html, name="from_markdown")
    app.add_template_filter(separate_names_by_space, name="sep_by_space")


def md_to_html(text):
    return markdown.markdown(text)


def separate_names_by_space(tags):
    names = map(lambda t: t.name, tags)
    return " ".join(names)
