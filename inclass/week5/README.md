# Week 5 in-class demo: user/state management

Sessions, hashing, MongoEngine and Flask-Login. Uses Flask 2.0.3 (same pins as the P4 starter), so make a **new virtual environment**; do not reuse Week 4's (Flask 3).

## Files

- `hash_demo.py`: fast hashes (SHA-256), timing, and a tiny rainbow table.
- `bcrypt_demo.py`: BCrypt salts, checking, and timing.
- `decode_cookie.py`: decodes a Flask session cookie to show it is readable (signed, not encrypted).
- `app.py`: the Flask app (register, log in, log out, protected notes page).
- `extensions.py`: `db`, `login_manager`, `bcrypt` objects, created once and attached in `app.py`.
- `models.py`: `User` and `Note` MongoEngine documents, plus the Flask-Login `user_loader`.
- `forms.py`: Flask-WTF registration, login and note forms.
- `templates/`: Jinja templates.
- `.env.example`: template for your secrets. `.flaskenv`: Flask settings (port 5005); it is not tracked by git (see `.gitignore`).

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
cp .env.example .env
```

Edit `.env`: set `MONGO_URI` to your Atlas connection string and `SECRET_KEY` to any long random string. Never commit `.env`.

## Run

```bash
flask run
```

`.flaskenv` sets port 5005; or use `flask run --port 5005`.

`hash_demo.py`, `bcrypt_demo.py` and `decode_cookie.py "<cookie value>"` run on their own with `python3` (the bcrypt demo needs the installed requirements, but no database).

## Note

This app uses **MongoEngine** (like P4). P3 uses Flask-PyMongo.
