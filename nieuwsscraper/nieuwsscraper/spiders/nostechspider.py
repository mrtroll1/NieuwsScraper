import scrapy
from nieuwsscraper import items
from datetime import datetime, timedelta


class NosTechSpider(scrapy.Spider):
    """A class to scrape weekly news of tech category"""
    name = "nostechspider"
    allowed_domains = ["nos.nl"]
    start_urls = ["https://nos.nl/nieuws/tech"]

    def is_this_week(self, article):
        time = article.css('time::attr(datetime)').get()
        time = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S%z")
        
        now = datetime.now(time.tzinfo)
        week_ago = now - timedelta(days=7)

        return week_ago <= time <= now

    def parse(self, response):
        article_item = items.ArticleItem()

        base_url = "nos.nl"
        for article in response.css('ul.sc-8a121b83-0.gETdJR.sc-7e9566f5-0.friZgz > li'):
            if self.is_this_week(article) == True:
                article_item['title'] = article.css('h2::text').get()
                relative_url = article.css('a::attr(href)').get()
                article_item['url'] = base_url + relative_url
                article_item['photo_url'] = article.css('img::attr(src)').get()
                article_item['description'] = article.css('p.sc-350b37b9-5.fLEHMx::text').get()
                yield article_item

        