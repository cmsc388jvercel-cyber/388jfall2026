# acid_demo.py -- Week 10, Part 4: why a transfer must be one transaction.
# isolation_level=None means "autocommit":
# every statement is its own tiny transaction until WE write BEGIN.
import sqlite3


def new_bank():
    db = sqlite3.connect(":memory:", isolation_level=None)
    db.execute("CREATE TABLE accounts (id INTEGER PRIMARY KEY, name TEXT, balance INTEGER NOT NULL CHECK (balance >= 0))")
    db.execute("INSERT INTO accounts VALUES (1, 'Alice', 20), (2, 'Bob', 30)")
    return db


def report(db, label):
    alice, bob = (r[0] for r in db.execute("SELECT balance FROM accounts ORDER BY id"))
    print(f"{label:<38} Alice={alice:<3} Bob={bob:<3} total={alice + bob}")


def transfer_no_transaction(db, amount, crash=False):
    db.execute("UPDATE accounts SET balance = balance + ? WHERE id = 2", (amount,))  # committed immediately
    if crash:
        raise RuntimeError("server crashed")
    db.execute("UPDATE accounts SET balance = balance - ? WHERE id = 1", (amount,))


def transfer(db, amount, crash=False):
    db.execute("BEGIN")
    try:
        db.execute("UPDATE accounts SET balance = balance + ? WHERE id = 2", (amount,))
        if crash:
            raise RuntimeError("server crashed")
        db.execute("UPDATE accounts SET balance = balance - ? WHERE id = 1", (amount,))
        db.execute("COMMIT")
    except Exception:
        db.execute("ROLLBACK")  # undo every statement since BEGIN
        raise


print("--- A. No transaction, and the server dies in the middle ---")
db = new_bank()
report(db, "before")
try:
    transfer_no_transaction(db, 10, crash=True)
except RuntimeError as e:
    print("error:", e)
report(db, "after (Bob got $10, Alice kept hers)")

print("\n--- B. The same crash, inside a transaction ---")
db = new_bank()
report(db, "before")
try:
    transfer(db, 10, crash=True)
except RuntimeError as e:
    print("error:", e)
report(db, "after (rolled back: nothing changed)")

print("\n--- C. A transfer that works ---")
transfer(db, 10)
report(db, "after transfer of 10")

print("\n--- D. Consistency: Alice only has 10 left, and tries to send 25 ---")
try:
    transfer(db, 25)
except sqlite3.IntegrityError as e:
    print("error:", e)
report(db, "after (Bob's +25 was undone too)")
