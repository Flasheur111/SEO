from flask import Blueprint, render_template, jsonify, request

from tools.rss_parser import RssParser

articles = Blueprint('articles', __name__, url_prefix='/articles')

@articles.route('/', methods=['GET'])
def get_articles():
    count =  int(request.args.get('count', '')) if request.args.get('count', '').isdigit() else None
    rp = RssParser()
    return jsonify(results=rp.get_news_urls(count))