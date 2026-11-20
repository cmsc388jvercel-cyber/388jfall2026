# app.py -- Week 10, Part 5: the bank from the textbook, as a tiny Flask app on port 5101.
# Needs: python3 db_setup.py (creates bank.db). POST routes are called by transfer_client.py or curl, not the browser.
import sqlite3

from flask import Flask, jsonify, request

app = Flask(__name__)


def get_db():
    db = sqlite3.connect("bank.db", isolation_level=None)  # autocommit, so BEGIN / COMMIT are ours to write
    db.row_factory = sqlite3.Row
    return db


@app.route("/accounts")
def accounts():
    db = get_db()
    rows = db.execute("SELECT id, name, balance FROM accounts").fetchall()
    return jsonify([dict(r) for r in rows])


@app.route("/total")
def total():
    """Helper route: the bank's total money. A correct bank never changes this number."""
    return jsonify(total=get_db().execute("SELECT SUM(balance) FROM accounts").fetchone()[0])


@app.route("/reset", methods=["POST"])
def reset():
    """Helper route: Alice = 20, Bob = 30 again."""
    db = get_db()
    db.execute("UPDATE accounts SET balance = 20 WHERE id = 1")
    db.execute("UPDATE accounts SET balance = 30 WHERE id = 2")
    return jsonify(ok=True)


@app.route("/transfer/<int:amount>", methods=["POST"])
def transfer(amount):
    """Move money from Alice (1) to Bob (2) in ONE transaction."""
    db = get_db()
    try:
        db.execute("BEGIN")
        db.execute("UPDATE accounts SET balance = balance + ? WHERE id = 2", (amount,))
        if request.args.get("crash"):  # pretend the server dies half way
            raise RuntimeError("server crashed")
        db.execute("UPDATE accounts SET balance = balance - ? WHERE id = 1", (amount,))
        db.execute("COMMIT")
        return jsonify(ok=True, amount=amount), 201
    except Exception as e:
        db.execute("ROLLBACK")
        return jsonify(ok=False, error=str(e)), 400


@app.route("/transfer_unsafe/<int:amount>", methods=["POST"])
def transfer_unsafe(amount):
    """The same transfer WITHOUT a transaction: each UPDATE commits by itself."""
    db = get_db()
    try:
        db.execute("UPDATE accounts SET balance = balance + ? WHERE id = 2", (amount,))
        if request.args.get("crash"):
            raise RuntimeError("server crashed")
        db.execute("UPDATE accounts SET balance = balance - ? WHERE id = 1", (amount,))
        return jsonify(ok=True, amount=amount), 201
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500  # no rollback: Bob already has the money


if __name__ == "__main__":
    app.run(port=5101)
