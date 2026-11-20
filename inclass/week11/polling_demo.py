# polling_demo.py -- Week 11, Part 1: what polling costs.
from flask import Flask, jsonify

app = Flask(__name__)
clock = {"now": 0}
MESSAGES = {3: "hello", 8: "anyone there?"}      # second -> new message arrives at that time


@app.route("/latest")
def latest():
    """The server only answers when asked. It cannot speak first."""
    new = {t: m for t, m in MESSAGES.items() if clock["now"] - 1 < t <= clock["now"]}
    return jsonify(new=list(new.values()))


client = app.test_client()
wasted = useful = 0
delays = []
print("second  request          answer")
for second in range(1, 11):                      # the browser asks once per second
    clock["now"] = second
    got = client.get("/latest").get_json()["new"]
    if got:
        useful += 1
        delays += [second - t for t in MESSAGES if second - 1 < t <= second]
    else:
        wasted += 1
    print(f"{second:>5}   GET /latest       {got if got else 'nothing new'}")

print()
print(f"requests sent: {wasted + useful}   useful: {useful}   wasted: {wasted}")
print("A message can wait up to a full second before the client even finds out.")
