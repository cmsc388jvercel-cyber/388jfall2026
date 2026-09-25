"""Week 4, Part 5: insert_many, find, filters, operators, and a unique index.

Run:  python3 queries_demo.py
It uses its own `people` collection and wipes it each run, so it is safe to repeat.
"""
import os

from dotenv import load_dotenv
from flask import Flask
from flask_pymongo import PyMongo
from pymongo.errors import DuplicateKeyError

load_dotenv()

app = Flask(__name__)
app.config["MONGO_URI"] = os.environ["MONGO_URI"]
mongo = PyMongo(app, serverSelectionTimeoutMS=5000)

mongo.db.people.drop()  # start clean every run

# ---- Many documents at once -------------------------------------------------
new_users = [
    {"name": "Yashas", "location": "Finland", "age": 42},
    {"name": "Kenton", "location": "Peru", "age": 31},
    {"name": "Maya", "location": "Canada", "age": 19},
]
mongo.db.people.insert_many(new_users)

# ---- find_one: a single dict, or None if nothing matches --------------------
print("\nfind_one({'name': 'Kenton'}):")
print(mongo.db.people.find_one({"name": "Kenton"}))

print("\nfind_one({'name': 'Nobody'}):")
print(mongo.db.people.find_one({"name": "Nobody"}))  # None

# ---- find: a cursor over every match ----------------------------------------
print("\nfind({'age': 31}):")
for person in mongo.db.people.find({"age": 31}):
    print(person["name"])

# ---- Operators start with $ -------------------------------------------------
print("\nfind({'age': {'$gt': 20}}):")
for person in mongo.db.people.find({"age": {"$gt": 20}}):
    print(person["name"])

# find() returns a cursor, not a list. Wrap it in list() to pass it to a template.
people = list(mongo.db.people.find())
print(f"\nlist(find()) gave a real list with {len(people)} documents")

# ---- A unique index ---------------------------------------------------------
mongo.db.people.create_index("name", unique=True)
print("\nIndexes now:", list(mongo.db.people.index_information()))

try:
    mongo.db.people.insert_one({"name": "Kenton", "location": "Spain", "age": 50})
except DuplicateKeyError:
    print("DuplicateKeyError: the unique index refused a second 'Kenton'")
