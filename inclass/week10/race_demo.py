# race_demo.py -- Week 10, Part 6: a race condition (lost update), and two ways to fix it.
# Two workers each withdraw $10 five times from one account that starts at $100. Ten withdrawals should leave $0.
import os
import sqlite3
import tempfile
import threading
import time

path = os.path.join(tempfile.mkdtemp(), "race.db")


def reset():
    db = sqlite3.connect(path)
    db.execute("DROP TABLE IF EXISTS accounts")
    db.execute("CREATE TABLE accounts (id INTEGER PRIMARY KEY, balance INTEGER)")
    db.execute("INSERT INTO accounts VALUES (1, 100)")
    db.commit()
    db.close()


def balance():
    return sqlite3.connect(path).execute("SELECT balance FROM accounts WHERE id = 1").fetchone()[0]


def run(worker, label):
    """Start two workers at the same time and wait for both."""
    reset()
    barrier = threading.Barrier(2)  # makes the two workers move in step, so the race happens EVERY time
    threads = [threading.Thread(target=worker, args=(barrier,)) for _ in range(2)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(f"{label:<36} expected 0, got {balance()}")


def read_then_write(barrier):
    """Read the balance into Python, work out the new one, write it back. Looks fine. Isn't."""
    db = sqlite3.connect(path, isolation_level=None, timeout=5)
    for _ in range(5):
        (bal,) = db.execute("SELECT balance FROM accounts WHERE id = 1").fetchone()
        barrier.wait()                    # both workers have now read the SAME number
        db.execute("UPDATE accounts SET balance = ? WHERE id = 1", (bal - 10,))
        barrier.wait()


def one_atomic_update(barrier):
    """Fix 1: let the database do the arithmetic. There is no gap between the read and the write."""
    db = sqlite3.connect(path, isolation_level=None, timeout=5)
    for _ in range(5):
        barrier.wait()
        db.execute("UPDATE accounts SET balance = balance - 10 WHERE id = 1")
        barrier.wait()


def locked_transaction(barrier):
    """Fix 2: keep read-then-write, but take the write lock BEFORE reading. The other worker must wait."""
    db = sqlite3.connect(path, isolation_level=None, timeout=5)
    for _ in range(5):
        db.execute("BEGIN IMMEDIATE")     # waits here until nobody else is writing
        (bal,) = db.execute("SELECT balance FROM accounts WHERE id = 1").fetchone()
        time.sleep(0.01)                  # the same gap as before, but now nobody can slip into it
        db.execute("UPDATE accounts SET balance = ? WHERE id = 1", (bal - 10,))
        db.execute("COMMIT")


run(read_then_write, "read, then write (race)")
run(one_atomic_update, "fix 1: balance = balance - 10")
run(locked_transaction, "fix 2: BEGIN IMMEDIATE (lock first)")
