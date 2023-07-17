import locale
import markdown
from pygments.formatters import HtmlFormatter

def format_date(object):
    locale.setlocale(locale.LC_ALL, "")
    return object.strftime("%d/%m/%Y")


def get_active_comments(object):
    active_comments = []
    for comment in object:
        if comment.active:
            active_comments.append(comment)
    return active_comments


def get_nbre_posts_by_category(object):
    publish_posts = []
    for post in object.posts:
        if post.publish:
            publish_posts.append(post)
    return len(publish_posts)


def pluralize(nbre, plural="s", singular=""):
    if nbre <= 1:
        return singular
    return plural


def format_markdown(object):
    md_template_string = markdown.markdown(object, extensions=["fenced_code", "codehilite"])
    formatter = HtmlFormatter(style="emacs", full=True, cssclass="codehilite")
    css_string = formatter.get_style_defs()
    md_css_string = "<style>" + css_string + "</style>"
    md_template = md_css_string + md_template_string
    return md_template



    