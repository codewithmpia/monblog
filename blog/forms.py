from flask_wtf import FlaskForm
from wtforms.fields import (
    StringField, EmailField, TextAreaField, 
    MultipleFileField, PasswordField, SubmitField
)
from wtforms.validators import DataRequired, Email


class CommentForm(FlaskForm):
    name = StringField(
        label="Votre nom",
        validators=[DataRequired()],
        render_kw={"class": "form-control"}
    )
    message = TextAreaField(
        label="Votre message",
        validators=[DataRequired()],
        render_kw={"class": "form-control"}
    )
    submit = SubmitField(label="Commenter")


class ContactForm(FlaskForm):
    name = StringField(
        label="Votre nom",
        validators=[DataRequired()],
        render_kw={"class": "form-control"}
    )
    email = EmailField(
        label="Votre adresse mail",
        validators=[DataRequired(), Email()],
        render_kw={"class": "form-control"}
    )
    message = TextAreaField(
        label="Votre message",
        validators=[DataRequired()],
        render_kw={"class": "form-control"}
    )
    submit = SubmitField(label="Envoyer")


class NewsLetterForm(FlaskForm):
    news_email = EmailField(
        label="Vaotre adresse mail",
        validators=[DataRequired(), Email()],
        render_kw={
            "placeholder": "Votre adresse mail",
            "class": "form-control"
        }
    )
    submit = SubmitField(label="S'abonner")


class EmailForm(FlaskForm):
    subject = StringField(
        label="Le sujet du mail",
        validators=[DataRequired()],
        render_kw={"class": "form-control"}
    )
    corps = TextAreaField(
        label="Le corps du mail",
        validators=[DataRequired()],
        render_kw={"class": "form-control"}
    )
    submit = SubmitField(label="Envoyer")


class LoginForm(FlaskForm):
    username = StringField(
        label="Nom d'utilisateur",
        validators=[DataRequired()],
        render_kw={"class": "form-control"}
    )
    password = PasswordField(
        label="Mot de passe",
        validators=[DataRequired()],
        render_kw={"class": "form-control"}
    )
    submit = SubmitField(label="Se connecter")



class UploadForm(FlaskForm):
    files = MultipleFileField(
        label="Vos fichiers",
        validators=[DataRequired()],
        render_kw={"class": "form-control"}
    )
    submit = SubmitField(label="Téléverser")
