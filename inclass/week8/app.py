# app.py -- Week 8: one tiny web server, started three times (ports 5081, 5082, 5083).
# Every copy runs this same file. Only the NAME and PORT differ, so we can see who answered.
import os
import sys
import time

from flask import Flask, jsonify, session

PORT = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 5081  # "flask run" passes "run", not a port
NAME = f"server-{PORT}"

app = Flask(__name__)
app.secret_key = "week8-demo-only"  # the SAME key on every copy, so any copy can read a cookie another copy signed

hits = 0  # lives in THIS process's memory only. Each copy has its own.


@app.route("/")
def index():
    return jsonify(served_by=NAME)


@app.route("/slow")
def slow():
    time.sleep(0.3)  # pretend this is an expensive page
    return jsonify(served_by=NAME, took="0.3s")


@app.route("/counter")
def counter():
    """STATEFUL on purpose: the count lives in this server's memory."""
    global hits
    hits += 1
    return jsonify(served_by=NAME, hits=hits)


@app.route("/visit")
def visit():
    """The count lives in the signed cookie, so it travels with the client to any server."""
    session["visits"] = session.get("visits", 0) + 1
    return jsonify(served_by=NAME, visits=session["visits"])


if __name__ == "__main__":
    app.run(port=PORT, debug=False, threaded=True)
