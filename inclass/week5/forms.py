from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import InputRequired, Length, Email, EqualTo, ValidationError

from models import User


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=40)])
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[InputRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        if User.objects(username=username.data).first() is not None:
            raise ValidationError("Username is taken")

    def validate_email(self, email):
        if User.objects(email=email.data).first() is not None:
            raise ValidationError("Email is taken")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Log In")


class NoteForm(FlaskForm):
    text = TextAreaField("Note", validators=[InputRequired(), Length(min=1, max=200)])
    submit = SubmitField("Save Note")
