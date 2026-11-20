# lock_demo.py -- Week 10, Part 6: what a lock looks like from the other connection's point of view.
import os
import sqlite3
import tempfile

path = os.path.join(tempfile.mkdtemp(), "lock.db")
setup = sqlite3.connect(path)
setup.execute("CREATE TABLE accounts (id INTEGER PRIMARY KEY, name TEXT, balance INTEGER)")
setup.execute("INSERT INTO accounts VALUES (1, 'Alice', 20)")
setup.commit()
setup.close()

writer = sqlite3.connect(path, isolation_level=None)
other = sqlite3.connect(path, isolation_level=None, timeout=0.2)  # give up after 0.2 s instead of waiting


def alice(db):
    return db.execute("SELECT balance FROM accounts WHERE id = 1").fetchone()[0]


print("1. nobody is writing (unlocked)")
print("   other reads Alice:", alice(other))

print("2. writer starts a transaction and changes Alice to 5, but does NOT commit yet")
writer.execute("BEGIN IMMEDIATE")
writer.execute("UPDATE accounts SET balance = 5 WHERE id = 1")
print("   writer sees Alice:", alice(writer))

print("3. the other connection tries to READ")
print("   other sees Alice:", alice(other), " <- the old value: it cannot see uncommitted changes (isolation)")

print("4. the other connection tries to WRITE")
try:
    other.execute("UPDATE accounts SET balance = 0 WHERE id = 1")
except sqlite3.OperationalError as e:
    print("   other is refused:", e)

print("5. writer commits")
writer.execute("COMMIT")

print("6. the other connection tries again")
other.execute("UPDATE accounts SET balance = balance - 1 WHERE id = 1")
print("   other wrote fine. Alice is now:", alice(other))
