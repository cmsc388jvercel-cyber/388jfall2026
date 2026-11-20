# join_demo.py -- Week 10, Part 2: JOIN, LEFT JOIN, and what happens if you forget ON.
from common import connect, show

db = connect("library.db")

print("=== 1. Two tables, side by side, no connection ===")
show(db.execute("SELECT * FROM sea_lions"), "sea_lions")
show(db.execute("SELECT * FROM migrations"), "migrations (sea_lion_id is the foreign key)")

print("=== 2. JOIN: match rows by the key ===")
show(db.execute("""
    SELECT sea_lions.name, migrations.from_place, migrations.to_place, migrations.km
    FROM sea_lions
    JOIN migrations ON migrations.sea_lion_id = sea_lions.id
"""), "every sea lion next to her trips")
# Sunny has two trips, so she appears twice. Pip has no trips, so Pip does not appear at all.

print("=== 3. LEFT JOIN: keep everyone from the left table ===")
show(db.execute("""
    SELECT sea_lions.name, migrations.to_place
    FROM sea_lions
    LEFT JOIN migrations ON migrations.sea_lion_id = sea_lions.id
"""), "Pip is back, with NULL where the trip would be")

print("=== 4. The same idea with books and ratings ===")
show(db.execute("""
    SELECT books.title, books.year, ratings.reader, ratings.stars
    FROM ratings
    JOIN books ON books.id = ratings.book_id
    WHERE books.title = 'Dune'
"""), "ratings for Dune")

print("=== 5. What if we forget the ON? ===")
n_books = db.execute("SELECT COUNT(*) FROM books").fetchone()[0]
n_ratings = db.execute("SELECT COUNT(*) FROM ratings").fetchone()[0]
n_all = db.execute("SELECT COUNT(*) FROM books, ratings").fetchone()[0]
print(f"{n_books} books x {n_ratings} ratings = {n_all} rows: every book paired with every rating, true or not")
