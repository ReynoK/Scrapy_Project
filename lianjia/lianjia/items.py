# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class RentingHouse(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    area = scrapy.Field()
    house_type = scrapy.Field()
    layer = scrapy.Field()
    subway = scrapy.Field()
    position = scrapy.Field()
    manager = scrapy.Field() 
