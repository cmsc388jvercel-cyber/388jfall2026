import os

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect
from flask_pymongo import PyMongo
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField
from wtforms.validators import InputRequired, NumberRange, Length, ValidationError

load_dotenv()  # reads MONGO_URI from a .env file in this folder or a parent folder

app = Flask(__name__)
# A brand-new random key every time the server starts. With FLASK_DEBUG=1,
# saving any file restarts the server, so refresh the browser after a save.
app.config['SECRET_KEY'] = os.urandom(16)

# The connection string comes from .env, never from the code.
app.config['MONGO_URI'] = os.environ['MONGO_URI']
# Give up after 5 seconds instead of hanging if Atlas can't be reached.
mongo = PyMongo(app, serverSelectionTimeoutMS=5000)

# Two accounts can never share a username, even if two requests arrive at the
# same moment. Creating an index that already exists does nothing.
mongo.db.accounts.create_index('username', unique=True)


class WelcomeForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(min=4, max=30)])
    location = StringField('Location', validators=[InputRequired(), Length(min=3, max=50)])
    age = IntegerField('Age', validators=[InputRequired(),
        NumberRange(min=1, max=140, message='Must be between 1 and 140')])
    submit = SubmitField('Submit')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Register')

    # Same custom validator as Week 3, but the lookup is now real.
    def validate_username(self, username):
        if mongo.db.accounts.find_one({'username': username.data}) is not None:
            raise ValidationError('That username is already taken')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = WelcomeForm()
    if form.validate_on_submit():
        user = {
            'name': form.name.data,
            'location': form.location.data,
            'age': form.age.data,
        }
        mongo.db.users.insert_one(user)
        return redirect(request.path)  # Post/Redirect/Get, same as Week 3

    message = None
    # Newest document first: sort by _id, descending.
    latest = mongo.db.users.find_one(sort=[('_id', -1)])
    if latest is not None:
        message = f'Welcome {latest["name"]} of {latest["location"]}'
    return render_template('index.html', message=message, form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # We only store the username. Passwords need hashing first (Week 5).
        mongo.db.accounts.insert_one({'username': form.username.data})
        return redirect(request.path)

    latest = mongo.db.accounts.find_one(sort=[('_id', -1)])
    registered = latest['username'] if latest is not None else None
    return render_template('register.html', form=form, registered=registered)


@app.route('/users')
def users():
    # find() gives back a cursor. list() turns it into something a template can loop over.
    all_users = list(mongo.db.users.find())
    return render_template('users.html', users=all_users)
