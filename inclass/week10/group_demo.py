# group_demo.py -- Week 10, Part 3: GROUP BY, aggregate functions, HAVING and ORDER BY.
from common import connect, show

db = connect("library.db")

print("=== 1. An aggregate with no grouping gives ONE number ===")
show(db.execute("SELECT ROUND(AVG(stars), 2) AS average_of_everything FROM ratings"))

print("=== 2. GROUP BY: one result per book ===")
show(db.execute("""
    SELECT book_id, ROUND(AVG(stars), 2) AS average_rating
    FROM ratings
    GROUP BY book_id
"""), "the textbook query (book_id is hard to read)")

print("=== 3. Join first to get titles, then group ===")
show(db.execute("""
    SELECT books.title, books.year, COUNT(*) AS n_ratings, ROUND(AVG(ratings.stars), 2) AS average_rating
    FROM ratings
    JOIN books ON books.id = ratings.book_id
    GROUP BY books.id
    ORDER BY average_rating DESC, books.id
"""), "best rated first")

print("=== 4. HAVING filters groups; WHERE filters rows ===")
show(db.execute("""
    SELECT books.title, books.year, COUNT(*) AS n_ratings, ROUND(AVG(ratings.stars), 2) AS average_rating
    FROM ratings
    JOIN books ON books.id = ratings.book_id
    GROUP BY books.id
    HAVING COUNT(*) >= 2
    ORDER BY average_rating DESC, books.id
"""), "HAVING COUNT(*) >= 2: a single 5-star rating no longer wins")
show(db.execute("""
    SELECT books.title, books.year, COUNT(*) AS n_ratings
    FROM ratings
    JOIN books ON books.id = ratings.book_id
    WHERE ratings.stars >= 4
    GROUP BY books.id
    ORDER BY n_ratings DESC, books.id
"""), "WHERE stars >= 4 runs BEFORE grouping: how many 4+ star ratings each book has")

print("=== 5. LEFT JOIN + GROUP BY: do not lose the book nobody rated ===")
show(db.execute("""
    SELECT books.title, books.year, COUNT(ratings.id) AS n_ratings
    FROM books
    LEFT JOIN ratings ON ratings.book_id = books.id
    GROUP BY books.id
    ORDER BY n_ratings ASC, books.id
    LIMIT 3
"""), "COUNT(ratings.id) counts real ratings only, so Kindred shows 0")
