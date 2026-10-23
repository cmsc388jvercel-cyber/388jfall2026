import os

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-change-me")
MONGODB_SETTINGS = {"host": os.environ["MONGO_URI"], "db": "week6"}
SITE_NAME = "Week 6 Demo"
