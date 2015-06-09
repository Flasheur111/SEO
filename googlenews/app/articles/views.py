from flask import Blueprint, render_template,\
                  jsonify, request, redirect, url_for

from app.articles.form import RegistrationForm
from app.tools.rss_parser import RssParser
from app.tools.article_parser import ArticleParser
from app.tools import lemmatization
from operator import itemgetter
import hashlib

articles = Blueprint('articles', __name__, url_prefix='/articles')

md5_categories = {'en': {}, 'fr': {}}

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

    return render_template('404.html',
                           categories=categoriess,
                           keywords_title=keywords_title,
                           keywords_content=keywords_content)

@articles.route('/<int:post_id>', methods=['GET'])
def get_post(post_id):
    from app.articles.models import Article

    Article.query.all()
    article = Article.query.filter(Article.id == post_id).first()
    article = article.to_dict()

    article['title'] = article['title']
    article['content'] = article['content']

    return render_template('/articles/content.html', article=article)

@articles.route('/post', methods=['GET', 'POST'])
def post_form():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.title.validate(form)\
            and form.content.validate(form):
        from app.database import db_session
        from app.articles.models import Article

        image_url = 'https://pbs.twimg.com/profile_images/378800000532546226/dbe5f0727b69487016ffd67a6689e75a.jpeg'

        if form.image.data != 'None':
            image_url = form.image.data

        a = Article(form.title.data, form.content.data, image_url)
        db_session.add(a)
        db_session.commit()

        return redirect(url_for('home.index'))

    rp = RssParser()
    categories = rp.get_categories()

    return render_template('/articles/post.html', form=form, categories=categories)

@articles.route('/keywords', methods=['GET'])
def get_keywords():
    import html

    lang = request.args.get('lang', '')
    category = request.args.get('category', '')
    count = int(request.args.get('count', '')) if request.args.get('count', '').isdigit() else None
    is_full = html.escape(request.args.get('is_full', ''))

    rp = RssParser()
    l = []

    print('----- Loading RSS -----')
    if is_full == 'true':
        ar = ArticleParser()
        l = [ar.get_corpus(a_link) for a_link in rp.get_news_urls(count, category=category, lang=lang)]
    else:
        l = rp.get_news_previews(count, category=category, lang=lang)

    article_rss = {elt['title']: elt['text'] for elt in l}
    print('----- RSS Loaded -----')

    print('----- Finding Keywords ------')
    if category in md5_categories.keys():
        hash = hashlib.md5()
        hash.update(bytes(str(article_rss.keys()), 'utf8'))
        if hash.digest() == md5_categories[lang][category][0]:
            return jsonify(results=md5_categories[lang][category][1])

    keywords_title, keywords_content = lemmatization.lemmatization_full_article(article_rss, lang=lang)
    data = dict({'title': keywords_title, 'content': keywords_content})

    print('----- Caching Result -----')
    hash = hashlib.md5()
    hash.update(bytes(str(article_rss.keys()), 'utf8'))
    md5_categories[lang][category] = (hash.digest(), data)

    print('----- Request Done ------')
    return jsonify(results=data)

@articles.route('/images/<string:query>', methods=['GET'])
def find_images(query):
    from app.tools.bingapi import BingSearchAPI

    my_key = "SEmNCypr5RJ6ayluEaHai/Y5GCizaO1wtPBTjrBJ2KI"
    mediaArray = []
    bing = BingSearchAPI(my_key)
    params = {'$format': 'json', '$top': 8, '$skip': 0}
    results = bing.search(query, params).json()

    for image in results['d']['results']:
        mediaArray.append({'url': image['MediaUrl'], 'name': image['Title']})
    return jsonify(images=mediaArray)

@articles.route('/contents', methods=['GET'])
def get_contents():

    count = int(request.args.get('count', '')) if request.args.get('count', '').isdigit() else None

    rp = RssParser()
    ar = ArticleParser()
    l = [a_link for a_link in rp.get_news_urls(count, category=request.args.get('category', ''))]

    return jsonify(rss=l)


