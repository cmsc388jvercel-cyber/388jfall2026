import os
from flask import Flask, render_template, request, redirect, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField
from wtforms.validators import InputRequired, NumberRange, Length, ValidationError

app = Flask(__name__)
# A brand-new random key every time the server starts. With FLASK_DEBUG=1,
# saving any file restarts the server, so refresh the browser after a save.
app.config['SECRET_KEY'] = os.urandom(16)

# Stand-in for a database. Next week this becomes a real MongoDB query.
TAKEN_USERNAMES = {'admin', 'testudo'}


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

    # Custom validator: "validate_" + the exact field name.
    # WTForms finds and runs it automatically inside validate_on_submit().
    def validate_username(self, username):
        # Real version: User.objects(username=username.data).first()
        if username.data.lower() in TAKEN_USERNAMES:
            raise ValidationError('That username is already taken')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = WelcomeForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['location'] = form.location.data
        return redirect(request.path)  # Post/Redirect/Get

    message = None
    if 'name' in session:
        message = f'Welcome {session["name"]} of {session["location"]}'
    return render_template('index.html', message=message, form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        session['registered'] = form.username.data
        return redirect(request.path)  # Post/Redirect/Get

    return render_template('register.html', form=form,
                           registered=session.get('registered'))
