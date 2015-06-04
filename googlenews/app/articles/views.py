from flask import Blueprint, render_template, jsonify, request

from app.tools.rss_parser import RssParser
from app.tools.article_parser import ArticleParser

articles = Blueprint('articles', __name__, url_prefix='/articles')

@articles.route('/', methods=['GET'])
def get_articles():
    count =  int(request.args.get('count', '')) if request.args.get('count', '').isdigit() else None
    rp = RssParser()
    ar = ArticleParser()
    l = [ ar.get_corpus(a_link) for a_link in rp.get_news_urls(count)]
    return jsonify(results=l)
