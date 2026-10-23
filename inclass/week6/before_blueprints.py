# before_blueprints.py -- Week 6, Part 1: one file, every route. Shown only to see the problem.
# Not part of the app. Run it with: python3 before_blueprints.py
from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "home"


@app.route("/about")
def about():
    return "about"


@app.route("/register")
def register():
    return "register"


@app.route("/login")
def login():
    return "login"


@app.route("/logout")
def logout():
    return "logout"


@app.route("/account")
def account():
    return "account"


# ...and this file keeps growing with every feature we add.
print(app.url_map)
