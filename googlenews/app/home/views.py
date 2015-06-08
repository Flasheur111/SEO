from flask import Blueprint, render_template

home = Blueprint('home', __name__, url_prefix='/home')

@home.route('/', methods=['GET'])
def index():
    from app.articles.models import Article

    ad = []

    for article in Article.query.all():
        article = article.to_dict()
        article['title'] = article['title']
        article['content'] = article['content']

        ad.append(article)

    return render_template('home/index.html', post_list=ad)
