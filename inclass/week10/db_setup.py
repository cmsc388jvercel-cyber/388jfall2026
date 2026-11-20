# db_setup.py -- Week 10: build library.db and bank.db from schema.sql. Run it once, and again any time you want a clean start.
import os
import sqlite3

sql = open("schema.sql").read()
library_sql, bank_sql = sql.split("--BANK--")

for name, script in [("library.db", library_sql), ("bank.db", bank_sql)]:
    if os.path.exists(name):
        os.remove(name)
    db = sqlite3.connect(name)
    db.executescript(script)
    db.commit()
    db.close()
    print("built", name)
