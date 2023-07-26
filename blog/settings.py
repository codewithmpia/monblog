from datetime import timedelta

from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_login import LoginManager, current_user
from flask_mail import Mail
from flask_assets import Environment

from .utils import BASE_DIR, css, js, get_env_vars as VAR

# Application initialization
blog = Flask(
    __name__,
    instance_path=BASE_DIR,
    template_folder=BASE_DIR / "assets/templates",
    static_folder=BASE_DIR / "assets/static"
)

# Secret key
blog.config["SECRET_KEY"] = VAR("SECRET_KEY", "top-secret")

# Session lifetime
blog.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=5)

# Upload folder
blog.config["UPLOAD_FOLDER"] = BASE_DIR / "assets/static/images/contents"

# Database config
blog.config["SQLALCHEMY_DATABASE_URI"] = VAR("DATABASE_URL", f"sqlite:///{BASE_DIR}/db.sqlite3")
db = SQLAlchemy(blog)

# Mail config
blog.config["MAIL_SERVER"]= VAR("MAIL_SERVER", "smtp.codewithmpia.fr")
blog.config["MAIL_PORT"] = VAR("MAIL_PORT", 666)
blog.config["MAIL_USERNAME"] = VAR("MAIL_USERNAME", "admin@codewithmpia.fr")
blog.config["MAIL_PASSWORD"] = VAR("MAIL_PASSWORD", "top-secret")
blog.config["MAIL_USE_TLS"] = False
blog.config["MAIL_USE_SSL"] = True
mail = Mail(blog)

# Assets
assets = Environment(blog)
assets.register("all_css", css)
assets.register("all_js", js)
css.build()
js.build()


# URLConfig et Views
from .import views
from .import auth

# Admin
from .import models
from .import admin as adm 

admin = Admin(
    blog, 
    name="CODEWITHMPIA.FR", 
    index_view=adm.CustomAdminIndexView(
        name="Administration", 
        template="admin/index.html",
    ), 
    template_mode="bootstrap4"
)

admin.add_views(
    adm.CategoryAdminView(models.Category, db.session, category="Blog"),
    adm.PostAdminView(models.Post, db.session, category="Blog"),
    adm.CommentAdminView(models.Comment, db.session, category="Blog"),
    adm.ProjectAdminView(models.Project, db.session),
    adm.ContactAdminView(models.Contact, db.session),
    adm.NewsLetterAdminView(models.Newsletter, db.session)
)


# Custom template filters
from .import filters 

blog.add_template_filter(filters.format_date, name="format_date")
blog.add_template_filter(filters.get_active_comments, name="active")
blog.add_template_filter(filters.get_nbre_posts_by_category, name="nbre_posts_by_category")
blog.add_template_filter(filters.pluralize, name="pluralize")
blog.add_template_filter(filters.format_markdown, name="format_markdown")


# Context processors
from .import context_processors as ctx

blog.context_processor(ctx.inject_last_posts)
blog.context_processor(ctx.inject_newsletter_form)
blog.context_processor(ctx.inject_date)
blog.context_processor(ctx.inject_site_name)


# Flask_Login
login_manager = LoginManager(blog)
login_manager.login_view = "login"
login_manager.login_message = "La connexion est requise."

@login_manager.user_loader
def load_user(id):
    return models.User.query.get(id)

@blog.before_request
def get_current_user():
    g.user = current_user
