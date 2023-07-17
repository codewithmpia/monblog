from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required

from .settings import blog
from .models import User
from .forms import LoginForm


@blog.route("/login/", methods=("GET", "POST"))
def login():
    if current_user.is_authenticated and current_user.is_admin:
        return redirect(request.referrer)
    
    form = LoginForm()

    if request.method == "POST" and form.validate_on_submit():
        username = form.username.data 
        password = form.password.data 

        user = User.query.filter_by(username=username).first()

        if not (user and user.check_password(password)):
            flash("Nom d'utitlisateur ou mot de passe invalide. Veuillez réessayer.", "warning")
            return redirect(url_for("login"))
        
        login_user(user)

        flash("Vous êtes connecté.", "success")
            
        return redirect(url_for("admin.index"))
    
    elif form.errors:
        flash(form.errors, "warning")

    return render_template("login.html", form=form)


@blog.route("/logout/")
@login_required
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash("Vous êtes déconnecté.", "success")
        return redirect(url_for("post_list"))
    return redirect(url_for("post_list"))
