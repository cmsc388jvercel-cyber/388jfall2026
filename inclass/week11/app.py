# app.py -- Week 11: a tiny chat room with Flask-SocketIO, on port 5102.
# Run: python3 app.py   then open http://localhost:5102 in TWO browser windows.
from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-only-change-me"
socketio = SocketIO(app, async_mode="threading")  # threading: no extra server to install

online = {}  # session id -> username


@app.route("/")
def index():
    return render_template("chat.html")


@app.route("/notify", methods=["POST"])
def notify():
    """An ordinary HTTP route that PUSHES to every browser. Nobody asked for this message."""
    text = (request.get_json(silent=True) or {}).get("text", "ping")
    socketio.emit("announcement", {"text": text})
    return jsonify(ok=True)


@socketio.on("connect")
def on_connect():
    print("connected:", request.sid)


@socketio.on("join")
def on_join(data):
    name = str(data.get("username", "")).strip()[:20] or "anonymous"
    online[request.sid] = name
    emit("user_joined", {"username": name, "online": len(online)}, broadcast=True)


@socketio.on("chat_message")
def on_chat_message(data):
    name = online.get(request.sid, "anonymous")
    text = str(data.get("text", ""))[:200]          # never trust the client: cap the length
    if text.strip():
        emit("chat_message", {"username": name, "text": text}, broadcast=True)


@socketio.on("who_am_i")
def on_who_am_i():
    """No broadcast: emit() with no extras answers only the client that asked."""
    emit("you_are", {"username": online.get(request.sid, "anonymous")})


@socketio.on("disconnect")
def on_disconnect():
    name = online.pop(request.sid, None)
    if name:
        emit("user_left", {"username": name, "online": len(online)}, broadcast=True)


if __name__ == "__main__":
    socketio.run(app, port=5102, allow_unsafe_werkzeug=True)
