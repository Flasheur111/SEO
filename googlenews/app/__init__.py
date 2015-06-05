from flask import Flask, render_template, url_for

# Defining the application object
app = Flask(__name__)

# Project configuration
app.config.from_object('config')

from app.database import init_db
init_db()

from app.database import db_session

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

# Basic error handler
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


# Importing modules
from app.home.views import home
from app.articles.views import articles

# Register blueprints
app.register_blueprint(home)
app.register_blueprint(articles)

# Basic route
@app.route('/')
def index():
    return url_for('home.index')
