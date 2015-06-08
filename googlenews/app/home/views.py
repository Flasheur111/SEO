from flask import Blueprint, render_template, jsonify, request

from app.tools.rss_parser import RssParser
from app.tools.article_parser import ArticleParser

from app.tools import lemmatization

from lxml import html

home = Blueprint('home', __name__, url_prefix='/home')

@home.route('/', methods=['GET'])
def index():
    from app.articles.models import Article

    ad = []

    for article in Article.query.all():
        article = article.to_dict()
        article['title'] = html.fromstring(article['title']).text_content()
        article['content'] = html.fromstring(article['content']).text_content()

        ad.append(article)

    return render_template('home/index.html', post_list=ad)
