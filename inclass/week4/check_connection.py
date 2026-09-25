"""Week 4: check that your app can reach your MongoDB Atlas cluster.

Run this right after you set up Atlas:

    pip3 install -r requirements.txt
    cp .env.example .env        # then paste your real connection string into .env
    python3 check_connection.py

If it prints "Connected!" you're ready for P3.
"""
import os
import sys

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import (
    ConfigurationError,
    OperationFailure,
    ServerSelectionTimeoutError,
)

load_dotenv()

uri = os.environ.get("MONGO_URI")
if not uri:
    sys.exit("No MONGO_URI found.")

if "<password>" in uri or "<db_password>" in uri:
    sys.exit("Your MONGO_URI still contains the <password> placeholder. Replace it with your database user's password.")

try:
    # Give up after 5 seconds instead of hanging for 30.
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    client.admin.command("ping")  # raises if we can't reach the cluster or log in

    db = client.get_default_database("week4_demo")
    db.hello.insert_one({"msg": "hello from Week 4"})
    latest = db.hello.find_one(sort=[("_id", -1)])
    print("Connected!")
    print(f"Database: {db.name}")
    print(f"Wrote and read back a document: {latest}")

except ServerSelectionTimeoutError:
    print("Could not reach the cluster. Most likely causes:")
    print("  1. Your IP address isn't allowed. In Atlas, open Network Access and add your current IP")
    print("     (or, for class only, allow access from anywhere).")
    print("  2. You're offline, or the cluster address in MONGO_URI is mistyped.")
    sys.exit(1)
except OperationFailure:
    print("Reached the cluster but couldn't log in. Check the username and password in MONGO_URI.")
    print("If your password has special characters like @ : / ? # you must percent-encode them,")
    print("or set a simpler password in Atlas (Database Access).")
    sys.exit(1)
except ConfigurationError as e:
    print(f"Your MONGO_URI looks malformed: {e}")
    sys.exit(1)
