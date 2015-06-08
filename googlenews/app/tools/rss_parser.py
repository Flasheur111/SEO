import feedparser

class RssParser:
    categories = {'A la une': None, 'Automobile': 'a', 'Economie': 'b', 'Chine': 'c',
                  'Culture': 'e', 'Gros Plan': 'ir', 'France': 'n', 'Sport': 's', 'Santé': 'm',
                  'Science/High-Tech': 't', 'International': 'w'}

    def get_news_urls(self, count=10, category='A la une', lang='fr'):
        rss_url = 'http://news.google.fr/news?pz=1&cf=all&ned=' + lang + '&hl=' + lang + '&output=rss'
        if category in self.categories.keys():
            rss_url += '&topic=' + self.categories[category]
        elif category in self.categories.values():
            rss_url += '&topic=' + category

        request = rss_url + '&num=' + str(count)
        news_feed = feedparser.parse(request)

        article_urls = []

        for post in news_feed.entries:
            redirect_article_url = post.links[0].href
            article_url = redirect_article_url.split('&url=')[1]
            article_urls.append(article_url)

        return article_urls

    def get_categories(self):
        return self.categories