import os
from werkzeug.utils import secure_filename

from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from flask_mail import Message

from .import forms 
from .settings import blog, db, mail
from .import utils
from .import models 


@blog.route("/")
@blog.route("/<string:category_slug>/<int:category_id>/")
def post_list(category_slug=None, category_id=None):
    category = None
    categories = models.Category.query.all()
    posts = models.Post.query.filter_by(publish=True).order_by(models.Post.date.desc())
    nbre_posts = posts.count()

    if category_id and category_slug:
        category = models.Category.query.get_or_404(category_id, category_slug)
        posts = posts.filter_by(category_id=category.id)

    page = request.args.get("page")

    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    posts = posts.paginate(page=page, per_page=10)

    return render_template(
        "post_list.html", 
        category=category, 
        categories=categories, 
        posts=posts, 
        nbre_posts=nbre_posts
    )
    

@blog.route("/posts/<int:post_id>/<string:post_slug>/", methods=("GET", "POST"))
def post_detail(post_id, post_slug):
    post = models.Post.query.get_or_404(post_id, post_slug)
    category = models.Category.query.get_or_404(post.category_id)

    form = forms.CommentForm()

    if request.method == "POST" and form.validate_on_submit():
        name = form.name.data 
        message = form.message.data 

        new_comment = models.Comment(
            name=name,
            message=message,
            post_id=post.id
        )

        msg = f"""
        Bonjour,
        Un commentaire de {name} est en attente de modération.
        Post: {post.title}
        Date: {post.date.strftime("%d/%m/%Y")}
        """

        utils.send_sms(msg)

        db.session.add(new_comment)
        db.session.commit()

        flash("Votre commentaire est en cours de modération.", "info")

        return redirect(url_for("post_detail", post_id=post.id, post_slug=post.slug))
        
    elif form.errors:
        flash(form.errors, "wanring")

    return render_template(
        "post_detail.html", 
        post=post, 
        category=category, 
        form=form
    )
    

@blog.route("/about/")
def about():
    projects = models.Project.query.filter_by(active=True).order_by(models.Project.date.desc())
    return render_template("about.html", projects=projects)
    

@blog.route("/contact/", methods=("GET", "POST"))
def contact():
    form = forms.ContactForm()

    if request.method == "POST" and form.validate_on_submit():
        name = form.name.data 
        email = form.email.data 
        message = form.message.data 

        new_contact = models.Contact(
            name=name,
            email=email,
            message=message
        )
        db.session.add(new_contact)
        db.session.commit()

        # End confirmation email
        msg = Message(
            subject="Confirmation réception de votre message",
            sender=blog.config["MAIL_USERNAME"],
            recipients=[email]
        )
        msg.html = render_template(
            "partials/confirmation_email.html", 
            name=name, message=message
        )
        msg.attach(
            filename="logo_main.jpg",
            content_type="image/jpg",
            data=url_for("static", filename="images/logo_main.jpg").encode()
        )
        mail.send(msg)
       
        flash("Votre message a été envoyé avec succès.", "success")

        return redirect(url_for('contact'))
        
    elif form.errors:
        flash(form.errors, "warning")

    return render_template("contact.html", form=form)


# Search
@blog.route("/search/")
def search():
    q = request.args.get("q")
    if q:
        posts = models.Post.query.filter(
                models.Post.title.contains(q)|
                models.Post.content.contains(q)|
                models.Post.resume.contains(q)
            ).filter_by(publish=True)
    else:
        posts = models.Post.query.filter_by(publish=True)
    return render_template("search.html", posts=posts, q=q)

    
# Get NewsLetter Data
@blog.route("/get_newsletter_data/", methods=("GET", "POST"))
def get_newsletter_data():
    if request.method == "POST":
        email = request.form.get("news_email")
        news = models.Newsletter(email=email)
        db.session.add(news)
        db.session.commit()
        flash("Vous êtes maintenant abonné.", "success")
        return redirect(request.referrer)
    return redirect(request.referrer)


@blog.route("/upload/", methods=("GET", "POST"))
@login_required
def upload_file():
    if request.method == "POST":
        if "files[]" not in request.files:
            flash("Aucun fichier n'a été sélectionné.", "warning")
            return redirect(url_for("upload_file"))
        
        files = request.files.getlist("files[]")
        
        for file in files:
            if file and utils.allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(blog.config["UPLOAD_FOLDER"], filename))
                flash(f"Fichiers: {filename} a été téléversé avec succès.", "success")
        return redirect(url_for("upload_file"))

    return render_template("upload.html")


@blog.route("/send_email/", methods=("GET", "POST"))
@login_required
def send_email_to_newsletter():
    emails = models.Newsletter.query.all()
    form = forms.EmailForm()

    if request.method == "POST" and form.validate_on_submit():
        subject = form.subject.data 
        corps = form.corps.data 
    
        msg = Message(
            subject=subject,
            sender=blog.config["MAIL_USERNAME"],
            recipients=[email.email for email in emails]
        )
        msg.html = render_template(
            "partials/mail_data.html",
            corps=corps
        )
        mail.send(msg)

        flash("Vos mails ont été envoyé avec succès.", "success")

        return redirect(url_for("send_email_to_newsletter"))
    
    elif form.errors:
        flash(form.errors, "warning")

    return render_template("newsletter.html", form=form)


# Errors
# 404 and 500
@blog.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@blog.errorhandler(500)
def server_error(error):
    return render_template("500.html"), 500


