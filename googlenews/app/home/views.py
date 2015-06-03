from flask import Blueprint, render_template
from tools import lemmatization

home = Blueprint('home', __name__, url_prefix='/home')

@home.route('/', methods=['GET'])
def index():
    #Pass the key words to the view
    categories = []
    key_words = {}
    #key_words = lemmatization.lemmatisation(array_rss, 2);
    return render_template('/home/index.html', categories=categories, key_words=key_words)
