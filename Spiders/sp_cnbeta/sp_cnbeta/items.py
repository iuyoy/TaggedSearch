# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class SpCnbetaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    links = scrapy.Field()
    date = scrapy.Field()
    author = scrapy.Field()
    content = scrapy.Field()
    picture = scrapy.Field()
    media = scrapy.Field()
    pass
