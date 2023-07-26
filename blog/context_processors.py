from datetime import datetime

from .models import Post
from .forms import NewsLetterForm

def inject_last_posts():
    return {"latest_posts": Post.query.filter_by(publish=True).order_by(Post.date.desc())[:4]}

def inject_newsletter_form():
    return {"newsletter_form": NewsLetterForm()}

def inject_date():
    return {"date": datetime.now()}

def inject_site_name():
    return {"site_name": "codewithmpia.fr"}