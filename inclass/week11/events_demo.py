# events_demo.py -- Week 11, Part 3: events, emit and broadcast, with no browser.
# Flask-SocketIO ships a fake client for tests, so three "people" can chat inside one script.
from app import app, socketio

alice = socketio.test_client(app)
bob = socketio.test_client(app)
cara = socketio.test_client(app)

for client, name in ((alice, "alice"), (bob, "bob"), (cara, "cara")):
    client.emit("join", {"username": name})

# throw away the join announcements so we only look at the chat
for c in (alice, bob, cara):
    c.get_received()

print("alice emits 'chat_message' once ...")
alice.emit("chat_message", {"text": "hi everyone"})

for name, c in (("alice", alice), ("bob", bob), ("cara", cara)):
    got = c.get_received()
    shown = [(e["name"], e["args"][0]) for e in got]
    print(f"  {name} received: {shown}")

print()
print("bob emits 'who_am_i' (a reply to the sender only, no broadcast) ...")
bob.emit("who_am_i")
for name, c in (("alice", alice), ("bob", bob), ("cara", cara)):
    got = c.get_received()
    print(f"  {name} received: {[(e['name'], e['args'][0]) for e in got]}")

print()
print("an empty message is ignored, and a 500-character message is cut to 200:")
bob.emit("chat_message", {"text": "   "})
bob.emit("chat_message", {"text": "x" * 500})
got = alice.get_received()
print("  alice received", len(got), "event, length", len(got[0]["args"][0]["text"]))
