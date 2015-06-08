from flask import Blueprint, render_template,\
                  jsonify, request, redirect, url_for

from app.articles.form import RegistrationForm
from app.tools.rss_parser import RssParser
from app.tools.article_parser import ArticleParser
from app.tools import lemmatization
from operator import itemgetter

articles = Blueprint('articles', __name__, url_prefix='/articles')

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
    print(form.image.data)
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

@articles.route('/all', methods=['GET'])
def get_all_post():

    print(request.args.get('category', ''))

    count = int(request.args.get('count', '')) if request.args.get('count', '').isdigit() else None

    rp = RssParser()
    ar = ArticleParser()
    l = [ar.get_corpus(a_link) for a_link in rp.get_news_urls(count, category=request.args.get('category', ''))]
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

@articles.route('/images/<string:query>', methods=['GET'])
def find_images(query):
    from app.tools.bingapi import BingSearchAPI

    my_key = "ofiH66W+uTTX65ME7FKhtd2XtgAHxNEljh+700JzqFs"
    mediaArray = []
    bing = BingSearchAPI(my_key)
    params = {'$format': 'json','$top': 8,'$skip': 0}
    results = bing.search(query, params).json()

    for image in results['d']['results']:
        mediaArray.append({'url': image['MediaUrl'], 'name': image['Title']})
    return jsonify(images=mediaArray)


