# Week 6 in-class demo: blueprints, factories, flashing, uploads, error pages

One small app (`flask_app/`) built the way P4 is built, plus four tiny scripts that run on their own. Uses Flask 2.0.3 (same pins as the P4 starter plus Pillow), so use the **same Week 5 virtual environment style**: a new venv, not Week 4's (Flask 3). Use Python 3.10 to 3.12; Pillow 10.1.0 has no wheel for 3.13.

## Files

- `before_blueprints.py`: the "one file, every route" problem (Part 1). Not part of the app.
- `flask_app/__init__.py`: the application factory `create_app()`, the extension objects, blueprint registration, and the 404 handler (Parts 1, 2, 6).
- `flask_app/main/routes.py`, `flask_app/users/routes.py`: the two blueprints. The `users` blueprint holds register, login, logout, and the account page with the upload form (Parts 1, 3, 4, 5).
- `flask_app/models.py`: `User` with an optional `profile_pic` `ImageField`, and the `user_loader`.
- `flask_app/forms.py`: registration, login, and `UpdateProfilePicForm` (`FileField` with `FileAllowed`).
- `flask_app/utils.py`: `image_to_data_uri()`, which turns the stored bytes into a base64 `data:` URI.
- `flask_app/templates/`: Jinja templates, including `404.html`.
- `factory_demo.py`: two apps from one factory, and a print of `url_map` (Part 2).
- `filename_demo.py`: what `secure_filename` does to hostile filenames (Part 4).
- `base64_demo.py`: base64 on a few bytes, and what a `data:` URI looks like (Part 5).
- `.env.example`: template for your secrets. `.flaskenv`: Flask settings (port 5006); it is not tracked by git (see `.gitignore`).

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

`.flaskenv` sets `FLASK_APP=run.py` and port 5006. Open http://localhost:5006.

`filename_demo.py`, `base64_demo.py` and `before_blueprints.py` need nothing but the installed requirements. `factory_demo.py` sets a placeholder `MONGO_URI` itself and never contacts the database.

## Note

This app uses **MongoEngine** (like P4). P3 uses Flask-PyMongo.
