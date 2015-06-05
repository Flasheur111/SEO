import feedparser

class RssParser:

    def get_news_urls(self, count = 10, category='all', lang='fr'):
        rss_url = 'http://news.google.fr/news?pz=1&cf=' + category + '&ned=' + lang + '&hl=' + lang  + '&output=rss';

        request = rss_url + '&num=' + str(count)
        news_feed = feedparser.parse(request)

        article_urls = []

        for post in news_feed.entries:
            redirect_article_url = post.links[0].href
            article_url = redirect_article_url.split('&url=')[1]
            article_urls.append(article_url)

        return article_urls