from newspaper import Article

class ArticleParser:

    def get_corpus(self, article_url):
        article = Article(article_url)
        article.download()

        article.parse()

        return (article.authors, article.publish_date, article.text, article.top_image)