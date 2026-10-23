from flask_login import UserMixin

from . import db, login_manager


class User(db.Document, UserMixin):
    username = db.StringField(required=True, unique=True, min_length=1, max_length=40)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True)  # the bcrypt hash, never the plain text
    profile_pic = db.ImageField()  # optional: the image bytes live in MongoDB

    def get_id(self):
        return self.username


@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()
