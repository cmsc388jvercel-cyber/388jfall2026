# keys_demo.py -- Week 10, Part 1: primary keys and foreign keys.
import sqlite3

from common import connect, show

db = connect("library.db")

print("=== 1. A title does not identify a book ===")
show(db.execute("SELECT id, title, author, year FROM books WHERE title = 'Emma'"), "two different books, same title")
show(db.execute("SELECT id, title FROM books WHERE id = 3"), "the primary key finds exactly one row")


print("=== 2. One flat table repeats everything ===")
flat = sqlite3.connect(":memory:")
flat.row_factory = sqlite3.Row
flat.execute("CREATE TABLE flat (title TEXT, author TEXT, year INTEGER, reader TEXT, stars INTEGER)")
rows = db.execute("""SELECT books.title, books.author, books.year, ratings.reader, ratings.stars
                     FROM ratings JOIN books ON books.id = ratings.book_id""")  # JOIN is the next part
flat.executemany("INSERT INTO flat VALUES (?, ?, ?, ?, ?)", [tuple(r) for r in rows])
show(flat.execute("SELECT * FROM flat WHERE title = 'Dune'"), "Dune, with its author and year copied onto every rating")

flat.execute("UPDATE flat SET author = 'F. Herbert' WHERE title = 'Dune' AND reader = 'ana'")  # fix ONE row...
show(flat.execute("SELECT DISTINCT title, author FROM flat WHERE title = 'Dune'"), "...and now the database disagrees with itself")


print("=== 3. Two tables: the author is stored once ===")
show(db.execute("SELECT * FROM books WHERE id = 1"), "books: one row for Dune")
show(db.execute("SELECT * FROM ratings WHERE book_id = 1"), "ratings: book_id points back at books.id (the foreign key)")


print("=== 4. The foreign key is enforced ===")
try:
    db.execute("INSERT INTO ratings (book_id, reader, stars) VALUES (99, 'zed', 5)")
except sqlite3.IntegrityError as e:
    print("rejected:", e)
try:
    db.execute("INSERT INTO ratings (book_id, reader, stars) VALUES (1, 'zed', 9)")
except sqlite3.IntegrityError as e:
    print("rejected:", e)


print("\n=== 5. Without PRAGMA foreign_keys = ON ===")
loose = sqlite3.connect(":memory:")  # same tables, but this connection never turned the pragma on
loose.executescript(open("schema.sql").read().split("--BANK--")[0])
loose.execute("INSERT INTO ratings (book_id, reader, stars) VALUES (99, 'zed', 5)")
print("accepted a rating for book 99, which does not exist:", loose.execute("SELECT * FROM ratings WHERE book_id = 99").fetchall())
