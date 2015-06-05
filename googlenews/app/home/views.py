from flask import Blueprint, render_template, jsonify, request

from app.tools.rss_parser import RssParser
from app.tools.article_parser import ArticleParser

from app.tools import lemmatization

home = Blueprint('home', __name__, url_prefix='/home')

@home.route('/', methods=['GET'])
def index():
    count = int(request.args.get('count', '')) if request.args.get('count', '').isdigit() else None
    rp = RssParser()
    ar = ArticleParser()
    l = [ar.get_corpus(a_link) for a_link in rp.get_news_urls(count)]
    article_rss = {elt['title']: elt['text'] for elt in l}
    # Pass the key words to the view
    categoriess = ['All', 'News', 'gjejjkgjjegkjgjkejk']
    keywords_title, keywords_content = lemmatization.lemmatisation_full_article(article_rss, k=1, lang='fr')
    keywords_title_2, keywords_content_2 = lemmatization.lemmatisation_full_article(article_rss, k=2, lang='fr')
    keywords_title_3, keywords_content_3 = lemmatization.lemmatisation_full_article(article_rss, k=3, lang='fr')
    keywords_title.update(keywords_title_2)
    keywords_title.update(keywords_title_3)
    keywords_content.update(keywords_content_2)
    keywords_content.update(keywords_content_3)

    return render_template('/home/index.html',
                           categories=categoriess,
                           keywords_title=keywords_title,
                           keywords_content=keywords_content)
