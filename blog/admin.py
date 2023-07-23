from flask import redirect, url_for
from flask_admin import AdminIndexView, expose
from flask_admin.form import ImageUploadField
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

from .utils import BASE_DIR


class CustomAdminIndexView(AdminIndexView):
    @expose("/")
    def index(self):
        if current_user.is_authenticated and current_user.is_admin:
            return super(CustomAdminIndexView, self).index()
        return redirect(url_for("login"))


class BaseModelMixin:
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin
    
    def inaccessible_callback(self, *args):
        return redirect(url_for('login'))
    

class CategoryAdminView(BaseModelMixin, ModelView):
    column_list = ["name", "posts"]
    form_excluded_columns = ["slug"]

    def on_model_change(self, form, model, is_created):
        if is_created:
            model.generate_slug()
        return super().on_model_change(form, model, is_created)

class PostAdminView(BaseModelMixin, ModelView):
    form_extra_fields = {"image": ImageUploadField(
        label="Image",
        base_path=BASE_DIR / "assets",
        relative_path="static/images/posts/",
        allowed_extensions=["png", "jpeg", "jpg", "gif"]
    )}
    column_list = ["id","title", "author", "publish", "comments"]
    form_excluded_columns = ["slug"]
    
    def on_model_change(self, form, model, is_created):
        if is_created:
            model.generate_slug()
        return super().on_model_change(form, model, is_created)


class CommentAdminView(BaseModelMixin, ModelView):
    column_exclude_list = ["message"]


class ProjectAdminView(BaseModelMixin, ModelView):
    form_extra_fields = {"image": ImageUploadField(
        label="Image",
        base_path=BASE_DIR / "assets",
        relative_path="static/images/projects/"
    )}


class ContactAdminView(BaseModelMixin, ModelView):
    pass


class NewsLetterAdminView(BaseModelMixin, ModelView):
    pass