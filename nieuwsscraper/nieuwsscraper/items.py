import scrapy

class ArticleItem(scrapy.Item):
    """General class for an article item"""
    url = scrapy.Field()
    title = scrapy.Field()
    photo_url = scrapy.Field()
    description = scrapy.Field()
