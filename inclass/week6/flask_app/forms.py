from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, Email, EqualTo, ValidationError

from PIL import Image

from .models import User


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


class UpdateProfilePicForm(FlaskForm):
    picture = FileField(
        "Profile picture",
        validators=[FileRequired(), FileAllowed(["jpg", "png"], "Images only: jpg or png")],
    )
    submit = SubmitField("Upload")

    def validate_picture(self, picture):
        # FileAllowed only looks at the extension. Ask Pillow whether this is really an image.
        try:
            Image.open(picture.data).verify()
        except Exception:
            raise ValidationError("That file is not a valid image.")
        finally:
            picture.data.seek(0)
