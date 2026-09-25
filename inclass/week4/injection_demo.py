"""Week 4, Part 5: Mongo operator injection, and the fix.

Start it:   flask --app injection_demo run --port 5004
Attack it:  ./attack.sh        (in a second terminal)

WARNING: passwords are stored in plain text here ONLY so the demo is easy to read.
Week 5 covers hashing. Never do this in a real app.
"""
import os

from dotenv import load_dotenv
from flask import Flask, request
from flask_pymongo import PyMongo

load_dotenv()

app = Flask(__name__)
app.config["MONGO_URI"] = os.environ["MONGO_URI"]
mongo = PyMongo(app, serverSelectionTimeoutMS=5000)

# One demo account, recreated every time the server starts.
mongo.db.demo_accounts.drop()
mongo.db.demo_accounts.insert_one({"username": "admin", "password": "hunter2"})


@app.post("/login-unsafe")
def login_unsafe():
    data = request.get_json()
    # BAD: whatever JSON the client sent goes straight into the query.
    user = mongo.db.demo_accounts.find_one(
        {"username": data["username"], "password": data["password"]}
    )
    return {"logged_in": user is not None}


@app.post("/login-safe")
def login_safe():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    # GOOD: insist on plain strings before they touch the query.
    if not isinstance(username, str) or not isinstance(password, str):
        return {"error": "username and password must be strings"}, 400
    user = mongo.db.demo_accounts.find_one({"username": username, "password": password})
    return {"logged_in": user is not None}
