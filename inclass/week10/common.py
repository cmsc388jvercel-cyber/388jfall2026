# common.py -- Week 10: two tiny helpers shared by the demo scripts.
import sqlite3


def connect(path="library.db"):
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row            # rows behave like dicts: row["title"]
    db.execute("PRAGMA foreign_keys = ON")  # SQLite ignores foreign keys unless you ask it not to
    return db


def show(rows, title=None):
    """Print query results as a small table."""
    if title:
        print(f"-- {title}")
    rows = [dict(r) for r in rows]
    if not rows:
        print("(no rows)\n")
        return
    cols = list(rows[0])
    cells = [[("NULL" if r[c] is None else str(r[c])) for c in cols] for r in rows]
    widths = [max(len(c), *(len(row[i]) for row in cells)) for i, c in enumerate(cols)]
    print("  ".join(c.ljust(w) for c, w in zip(cols, widths)))
    print("  ".join("-" * w for w in widths))
    for row in cells:
        print("  ".join(v.ljust(w) for v, w in zip(row, widths)))
    print()
