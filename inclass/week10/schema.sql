-- schema.sql -- Week 10: the tables used by the library demos (library.db) and the bank demos (bank.db).
-- db_setup.py runs the two halves below. Nothing here is random, so everyone gets the same numbers.

-- ===== library.db =====

CREATE TABLE books (
    id     INTEGER PRIMARY KEY,          -- primary key: unique, never changes, assigned by the database
    title  TEXT NOT NULL,
    author TEXT NOT NULL,
    year   INTEGER
);

CREATE TABLE ratings (
    id      INTEGER PRIMARY KEY,
    book_id INTEGER NOT NULL REFERENCES books(id),   -- foreign key: must be the id of a real book
    reader  TEXT NOT NULL,
    stars   INTEGER NOT NULL CHECK (stars BETWEEN 1 AND 5)
);

CREATE TABLE sea_lions (
    id   INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age  INTEGER
);

CREATE TABLE migrations (
    id           INTEGER PRIMARY KEY,
    sea_lion_id  INTEGER NOT NULL REFERENCES sea_lions(id),
    from_place   TEXT NOT NULL,
    to_place     TEXT NOT NULL,
    km           INTEGER
);

INSERT INTO books (id, title, author, year) VALUES
    (1, 'Dune',         'Frank Herbert',   1965),
    (2, 'Emma',         'Jane Austen',     1815),
    (3, 'Emma',         'Jane Austen',     2012),   -- a newer edition: same title, same author, different book
    (4, 'Neuromancer',  'William Gibson',  1984),
    (5, 'Beloved',      'Toni Morrison',   1987),
    (6, 'The Hobbit',   'J.R.R. Tolkien',  1937),
    (7, 'Piranesi',     'Susanna Clarke',  2020),
    (8, 'Kindred',      'Octavia Butler',  1979);   -- nobody has rated this one yet

INSERT INTO ratings (book_id, reader, stars) VALUES
    (1, 'ana', 5), (1, 'ben', 4), (1, 'cy', 5), (1, 'dee', 3), (1, 'eli', 5),
    (2, 'ana', 4), (2, 'ben', 3),
    (3, 'cy', 5),
    (4, 'ben', 4), (4, 'dee', 4), (4, 'eli', 5),
    (5, 'ana', 5), (5, 'cy', 4),
    (6, 'ana', 3), (6, 'ben', 3), (6, 'cy', 2), (6, 'dee', 4),
    (7, 'dee', 5);

-- made-up toy data for the textbook's sea lion example
INSERT INTO sea_lions (id, name, age) VALUES
    (1, 'Sunny',  9),
    (2, 'Marlow', 12),
    (3, 'Pip',    1),    -- a pup: has not migrated yet
    (4, 'Juno',   7);

INSERT INTO migrations (sea_lion_id, from_place, to_place, km) VALUES
    (1, 'Channel Islands', 'Monterey Bay',  520),
    (1, 'Monterey Bay',    'Channel Islands', 520),   -- Sunny has two trips, so she appears twice in a JOIN
    (2, 'Channel Islands', 'Oregon coast',  1100),
    (4, 'Channel Islands', 'Puget Sound',   1700);

-- ===== bank.db =====
-- (db_setup.py splits the file at the next marker line)
--BANK--
CREATE TABLE accounts (
    id      INTEGER PRIMARY KEY,
    name    TEXT NOT NULL,
    balance INTEGER NOT NULL CHECK (balance >= 0)    -- the database itself refuses a negative balance
);

INSERT INTO accounts (id, name, balance) VALUES (1, 'Alice', 20), (2, 'Bob', 30);
