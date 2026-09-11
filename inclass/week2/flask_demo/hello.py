# Part 1: bare minimum Flask app, basic routing, variable routing.
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route("/index")
def hello_world():
    return render_template('base.html', title="STIC")






@app.route("/about")
def about():
    return "this class is fun"

@app.route("/u/<username>")
def show_profile(username):
    return "this is {}'s profile".format(username)

# Part 3A: templating basics -- rendering a static template.

@app.route('/bad-example')

def bad_example():
    return '''
    <html>
        <body>
            This is a <b> bad example </b>
        </body>
    </html>
    '''
# Part 3B: templating with real data -- feeding a template from Python.

posts = [
    {'user': 'John Conner', 'text': 'The sun is a reactor', 'likes': '2'},
    {'user': 'Roshan', 'text': 'This class is fun!!','likes': 'inf'},
    {'user': 'rushil', 'text': 'flask is cool', 'likes': '5000'}
]

@app.route('/feed')
def feed():
    return render_template('posts.html', title="STICs", posts=posts)
