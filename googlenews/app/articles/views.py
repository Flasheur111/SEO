from flask import Blueprint, render_template, jsonify, request

from app.tools.rss_parser import RssParser
from app.tools.article_parser import ArticleParser
from app.tools import lemmatization

articles = Blueprint('articles', __name__, url_prefix='/articles')

@articles.route('/get', methods=['GET'])
def get_articles():
    count = int(request.args.get('count', '')) if request.args.get('count', '').isdigit() else None
    rp = RssParser()
    ar = ArticleParser()
    l = [ar.get_corpus(a_link) for a_link in rp.get_news_urls(count)]
    return jsonify(results=l)

@articles.route('/', methods=['GET'])
def index():
    count = int(request.args.get('count', '')) if request.args.get('count', '').isdigit() else None
    rp = RssParser()
    ar = ArticleParser()
    l = [ar.get_corpus(a_link) for a_link in rp.get_news_urls(count)]
    article_rss = {elt.title: elt.text for elt in l}
    #Pass the key words to the view
    categories = ['All', 'News']
    keywords_title, keywords_content = lemmatization.lemmatisation_full_article(article_rss, 2);
    return render_template('/home/index.html', categories=categories, keywords_title=keywords_title, keywords_content=keywords_content)

