from datetime import datetime

from flask_login import UserMixin

from extensions import db, login_manager


class User(db.Document, UserMixin):
    username = db.StringField(required=True, unique=True, min_length=1, max_length=40)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True)  # the bcrypt hash, never the plain text

    # Flask-Login stores this string in the session cookie.
    def get_id(self):
        return self.username


class Note(db.Document):
    author = db.ReferenceField(User, required=True)
    text = db.StringField(required=True, max_length=200)
    created = db.DateTimeField(default=datetime.utcnow)


# Flask-Login calls this on every request to turn the cookie's id back into a User.
@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()
