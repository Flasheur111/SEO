from flask import Blueprint, render_template,\
                  jsonify, request, flash, redirect, url_for

from app.articles.form import RegistrationForm
from app.tools.rss_parser import RssParser
from app.tools.article_parser import ArticleParser
from app.tools import lemmatization
from operator import itemgetter

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

    return render_template('/articles/content.html', article=a.to_dict())

@articles.route('/post', methods=['GET', 'POST'])
def post_form():
    form = RegistrationForm(request.form)
    print(form.image.data)
    if request.method == 'POST' and form.validate():
        flash('Thanks for registering')
        return redirect(url_for('home.homepage'))

    rp = RssParser()
    categories = rp.get_categories()

    return render_template('/articles/post.html', form=form, categories=categories)

@articles.route('/all', methods=['GET'])
def get_all_post():
    from app.articles.models import Article

    print(request.args.get('category', ''))

    count = int(request.args.get('count', '')) if request.args.get('count', '').isdigit() else None

    ad = [a.to_dict() for a in Article.query.all()]
    rp = RssParser()
    ar = ArticleParser()
    l = [ar.get_corpus(a_link, ) for a_link in rp.get_news_urls(count, category=request.args.get('category', ''))]
    article_rss = {elt['title']: elt['text'] for elt in l}

    keywords_title, keywords_content = lemmatization.lemmatisation_full_article(article_rss, k=1, lang='fr')
    keywords_title_2, keywords_content_2 = lemmatization.lemmatisation_full_article(article_rss, k=2, lang='fr')
    keywords_title_3, keywords_content_3 = lemmatization.lemmatisation_full_article(article_rss, k=3, lang='fr')
    keywords_title.update(keywords_title_2)
    keywords_title.update(keywords_title_3)
    keywords_content.update(keywords_content_2)
    keywords_content.update(keywords_content_3)

    keywords_title = [key[0] for key in sorted(keywords_title.items(), key=itemgetter(1), reverse=True)]
    keywords_content = [key[0] for key in sorted(keywords_content.items(), key=itemgetter(1), reverse=True)]
    data = dict({'title': keywords_title, 'content': keywords_content})
    return jsonify(results=data)


