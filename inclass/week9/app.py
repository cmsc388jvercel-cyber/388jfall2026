# app.py -- Week 9: the "origin" server on port 5091. Every demo this week talks to it, directly or through proxy.py.
import hashlib
import time

from flask import Flask, jsonify, make_response, request

app = Flask(__name__)

built = {"clock": 0, "live": 0}                                        # how many times this server REALLY built each response
article = {"version": 1, "title": "Inception", "text": "A thief enters dreams."}  # a pretend database row


@app.route("/")
def index():
    """What does the origin see? Behind a proxy, the connection comes from the proxy, not the user."""
    return jsonify(
        remote_addr=request.remote_addr,
        x_forwarded_for=request.headers.get("X-Forwarded-For"),
        via=request.headers.get("Via"),
    )


@app.route("/reset")
def reset():
    """Helper route: set the 'built' counters back to zero."""
    built["clock"] = built["live"] = 0
    return jsonify(ok=True)


@app.route("/slow")
def slow():
    """An expensive page. Allowed to be cached for 5 seconds."""
    time.sleep(0.3)
    resp = jsonify(page="slow", took="0.3s")
    resp.headers["Cache-Control"] = "max-age=5"
    return resp


@app.route("/clock")
def clock():
    """Allowed to be cached for 5 seconds. 'built' goes up only when this function really runs."""
    built["clock"] += 1
    resp = jsonify(built=built["clock"], time=time.strftime("%H:%M:%S"))
    resp.headers["Cache-Control"] = "max-age=5"
    return resp


@app.route("/live")
def live():
    """Must never be stored by anyone."""
    built["live"] += 1
    resp = jsonify(built=built["live"], time=time.strftime("%H:%M:%S"))
    resp.headers["Cache-Control"] = "no-store"
    return resp


def current_etag():
    return '"' + hashlib.md5(repr(article).encode()).hexdigest()[:8] + '"'  # changes whenever the article changes


@app.route("/article")
def get_article():
    """Cache-Control: no-cache means 'you may keep a copy, but ask me before you reuse it'."""
    etag = current_etag()
    if request.headers.get("If-None-Match") == etag:
        resp = make_response("", 304)  # nothing changed: no body at all
    else:
        resp = jsonify(article)
    resp.headers["ETag"] = etag
    resp.headers["Cache-Control"] = "no-cache"
    return resp


@app.route("/article", methods=["POST"])
def edit_article():
    article["version"] += 1
    article["text"] = request.get_json()["text"]
    return jsonify(article)


@app.route("/assets/v<int:n>/style.css")
def versioned_file(n):
    """Versioned data: this URL's contents never change, so it can be cached for a year."""
    resp = make_response(f"/* style version {n} */ body {{ color: navy; }}")
    resp.headers["Content-Type"] = "text/css"
    resp.headers["Cache-Control"] = "public, max-age=31536000, immutable"
    return resp


if __name__ == "__main__":
    app.run(port=5091, debug=False, threaded=True)
