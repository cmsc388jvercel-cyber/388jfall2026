import os

from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user

from extensions import db, login_manager, bcrypt
from models import User, Note
from forms import RegistrationForm, LoginForm, NoteForm

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-only-change-me")
app.config["MONGODB_SETTINGS"] = {"host": os.environ["MONGO_URI"], "db": "week5"}

db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "login"  # where @login_required sends anonymous users


def is_safe_next(target):
    # Only allow paths on our own site, never a full URL to somewhere else.
    return target is not None and target.startswith("/") and not target.startswith(("//", "/\\"))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        User(username=form.username.data, email=form.email.data, password=hashed).save()
        flash("Account created. Please log in.")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(username=form.username.data).first()
        if user is not None and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get("next")
            return redirect(next_page if is_safe_next(next_page) else url_for("notes"))
        flash("Login failed. Check your username and password.")
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/notes", methods=["GET", "POST"])
@login_required
def notes():
    form = NoteForm()
    if form.validate_on_submit():
        Note(author=current_user._get_current_object(), text=form.text.data).save()
        return redirect(url_for("notes"))
    my_notes = Note.objects(author=current_user._get_current_object()).order_by("-created")
    return render_template("notes.html", form=form, notes=my_notes)
