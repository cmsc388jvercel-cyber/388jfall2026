# rooms_demo.py -- Week 11, Part 3: rooms. A room is a named group of connections.
from flask import Flask
from flask_socketio import SocketIO, emit, join_room

app = Flask(__name__)
socketio = SocketIO(app, async_mode="threading")


@socketio.on("join_room")
def on_join_room(data):
    join_room(data["room"])                      # this connection is now in that room


@socketio.on("say")
def on_say(data):
    emit("said", {"text": data["text"]}, to=data["room"])   # only that room hears it


alice, bob, cara = (socketio.test_client(app) for _ in range(3))
alice.emit("join_room", {"room": "lobby"})
bob.emit("join_room", {"room": "lobby"})
cara.emit("join_room", {"room": "ops"})

print("alice says 'hi lobby' to the lobby room ...")
alice.emit("say", {"room": "lobby", "text": "hi lobby"})
for name, c in (("alice", alice), ("bob", bob), ("cara", cara)):
    print(f"  {name} received: {[(e['name'], e['args'][0]['text']) for e in c.get_received()]}")

print()
print("the server pushes to room 'ops' (socketio.emit, outside any handler) ...")
socketio.emit("said", {"text": "deploy at 5"}, to="ops")
for name, c in (("alice", alice), ("bob", bob), ("cara", cara)):
    print(f"  {name} received: {[(e['name'], e['args'][0]['text']) for e in c.get_received()]}")
