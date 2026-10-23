from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user

from .. import bcrypt
from ..forms import RegistrationForm, LoginForm, UpdateProfilePicForm
from ..models import User
from ..utils import image_to_data_uri

users = Blueprint("users", __name__)


def is_safe_next(target):
    return target is not None and target.startswith("/") and not target.startswith(("//", "/\\"))


@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        User(username=form.username.data, email=form.email.data, password=hashed).save()
        flash("Account created. Please log in.")
        return redirect(url_for("users.login"))
    return render_template("register.html", form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(username=form.username.data).first()
        if user is not None and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get("next")
            return redirect(next_page if is_safe_next(next_page) else url_for("users.account"))
        flash("Login failed. Check your username and password.")
    return render_template("login.html", form=form)


@users.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You are logged out.")
    return redirect(url_for("main.index"))


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateProfilePicForm()
    if form.validate_on_submit():
        picture = form.picture.data
        user = current_user._get_current_object()
        if user.profile_pic:
            user.profile_pic.replace(picture, content_type=picture.content_type)
        else:
            user.profile_pic.put(picture, content_type=picture.content_type)
        user.save()
        flash("Profile picture updated.")
        return redirect(url_for("users.account"))
    pic = image_to_data_uri(current_user.profile_pic)
    return render_template("account.html", form=form, pic=pic)
