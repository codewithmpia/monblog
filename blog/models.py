from datetime import datetime
from slugify import slugify
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin

from .settings import db


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True)
    posts = db.relationship("Post", backref="category")

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.generate_slug()

    def generate_slug(self):
        if self.name:
            self.slug = slugify(self.name)
        else:
            self.slug = ""

    def __str__(self):
        return self.name


class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer(), primary_key=True)
    category_id = db.Column(db.Integer(), db.ForeignKey("categories.id"))
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True)
    author = db.Column(db.String(100), default="codewithmpia")
    resume = db.Column(db.Text(500), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    image = db.Column(db.Unicode(128))
    date = db.Column(db.DateTime(), default=datetime.utcnow())
    publish = db.Column(db.Boolean(), default=False)
    comments = db.relationship("Comment", backref="post")

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.generate_slug()

    def generate_slug(self):
        if self.title:
            self.slug = slugify(self.title)
        else:
            self.slug = ""
    
    def __str__(self):
        return self.title
    

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer(), primary_key=True)
    post_id = db.Column(db.Integer(), db.ForeignKey("posts.id"))
    name = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text(), nullable=False)
    date = db.Column(db.DateTime(), default=datetime.utcnow())
    active = db.Column(db.Boolean(), default=False)

    def __str__(self):
        return self.name
    

class Filter(db.Model):
    __tablename__ = "filters"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True)
    projects = db.relationship("Project", backref="filter")

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.generate_slug()

    def generate_slug(self):
        if self.name:
            self.slug = slugify(self.name)
        else:
            self.slug = ""

    def __str__(self):
        return self.name
    

class Project(db.Model):
    __tablename__ = "projects"
    id = db.Column(db.Integer(), primary_key=True)
    filter_id = db.Column(db.Integer(), db.ForeignKey("filters.id"))
    title = db.Column(db.String(255), nullable=False)
    image = db.Column(db.Unicode(128))
    url = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime(), default=datetime.utcnow())
    active = db.Column(db.Boolean(), default=False)

    def __str__(self):
        return self.title
    

class Contact(db.Model):
    __tablename__ = "contacts"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text(), nullable=False)
    date = db.Column(db.DateTime(), default=datetime.utcnow())

    def __str__(self):
        return self.name
    

class Newsletter(db.Model):
    __tablename__ = "newsletters"
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(100), nullable=False)

    def __str__(self):
        return self.email
    

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(255))
    is_admin = db.Column(db.Boolean(), default=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def check_password(self, password2):
        return check_password_hash(self.password, password2)
    
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True
    
    def __str__(self):
        return self.username
    