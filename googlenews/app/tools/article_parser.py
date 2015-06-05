from newspaper import Article, ArticleException


class ArticleParser:

    def get_corpus(self, article_url):
        article = Article(article_url)
        article.download()
        try:
            article.parse()
        except ArticleException:
            return {}
        return {'title': 'TTT', 'authors': article.authors, 'publish_date': article.publish_date, 'text': article.text, 'image': article.top_image}
