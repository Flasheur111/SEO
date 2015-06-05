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
    article_rss = {elt['title']: elt['text'] for elt in l}
    # Pass the key words to the view
    categoriess = ['All', 'News', 'gjejjkgjjegkjgjkejk']
    keywords_title, keywords_content = lemmatization.lemmatisation_full_article(article_rss, 2);
    print(keywords_title)
    print(keywords_content)
    return render_template('404.html',
                           categories=categoriess,
                           keywords_title=keywords_title,
                           keywords_content=keywords_content)

@articles.route('/db', methods=['GET'])
def db():
    from app.database import db_session
    from app.articles.models import Article

    a = Article('The end is near!', 'lmdsflksdfnsdlknf', 'hfgh')
    db_session.add(a)
    db_session.commit()

    return jsonify(results=a.to_dict())

@articles.route('/<int:post_id>', methods=['GET'])
def get_post(post_id):
    from app.articles.models import Article

    Article.query.all()
    a = Article.query.filter(Article.id == post_id).first()

    return jsonify(results=a.to_dict())

@articles.route('/all', methods=['GET'])
def get_all_post():
    from app.articles.models import Article

    count = int(request.args.get('count', '')) if request.args.get('count', '').isdigit() else None

    ad = [a.to_dict() for a in Article.query.all()]

    return jsonify(results=ad)


