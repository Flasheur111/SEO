from flask import Blueprint, render_template
from app.tools import lemmatization

home = Blueprint('home', __name__, url_prefix='/home')

@home.route('/', methods=['GET'])
def index():
    #Pass the key words to the view
    categories = []
    key_words = {}
    keywords_title, keywords_content = lemmatization.lemmatisation_full_article(array_rss, 2);
    return render_template('/home/index.html', categories=categories, key_words=key_words)

