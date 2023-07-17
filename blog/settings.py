from datetime import timedelta

from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_login import LoginManager, current_user
from flask_assets import Environment

from .utils import BASE_DIR, css, js, get_env_vars as VAR


blog = Flask(
    __name__,
    instance_path=BASE_DIR,
    template_folder=BASE_DIR / "assets/templates",
    static_folder=BASE_DIR / "assets/static"
)
# Secret key
blog.config["SECRET_KEY"] = VAR("SECRET_KEY", "top-secret")
blog.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=5)
blog.config["UPLOAD_FOLDER"] = BASE_DIR / "assets/static/uploads"

# Database
blog.config["SQLALCHEMY_DATABASE_URI"] = VAR("DATABASE_URL", f"sqlite:///{BASE_DIR}/db.sqlite3")
db = SQLAlchemy(blog)

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
    name="admin", 
    index_view=adm.CustomAdminIndexView(
        name="Accueil",
        template="admin/index.html",
    ), 
    template_mode="bootstrap4"
)

admin.add_views(
    adm.CategoryAdminView(models.Category, db.session, category="Blog"),
    adm.PostAdminView(models.Post, db.session, category="Blog"),
    adm.CommentAdminView(models.Comment, db.session, category="Blog"),
    adm.FilterAdminView(models.Filter, db.session,  category="Folio"),
    adm.ProjectAdminView(models.Project, db.session, category="Folio"),
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
blog.context_processor(ctx.inject_year)
blog.context_processor(ctx.inject_site_name)


# Flask_Login
login_manager = LoginManager(blog)
login_manager.login_view = "login"
login_manager.login_message = "Vous devez vous connecter pour accéder à cette page."

@login_manager.user_loader
def load_user(id):
    return models.User.query.get(id)

@blog.before_request
def get_current_user():
    g.user = current_user
