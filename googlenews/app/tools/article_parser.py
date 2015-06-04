from newspaper import Article

class ArticleParser:

    def get_corpus(self, article_url):
        article = Article(article_url)
        article.download()

        article.parse()

        return {'authors': article.authors, 'publish_date': article.publish_date, 'text': article.text, 'image': article.top_image}
