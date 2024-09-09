# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticleItem(scrapy.Item):
    """General class for an article item"""
    url = scrapy.Field()
    title = scrapy.Field()
    photo_url = scrapy.Field()
    description = scrapy.Field()
