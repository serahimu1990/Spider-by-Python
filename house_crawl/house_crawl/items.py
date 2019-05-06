# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# class NewHouseItem(scrapy.Item):
#     # define the fields for your item here like:
#     name = scrapy.Field()
#     rooms = scrapy.Field()
#     area = scrapy.Field()
#     address = scrapy.Field()
#     district = scrapy.Field()
#     sale = scrapy.Field()
#     price = scrapy.Field()
#     house_url = scrapy.Field()
#     province = scrapy.Field()
#     city = scrapy.Field()

class SecondHouseItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    rooms = scrapy.Field()
    area = scrapy.Field()
    address = scrapy.Field()
    unit = scrapy.Field()
    floor = scrapy.Field()
    toward = scrapy.Field()
    price = scrapy.Field()
    house_url = scrapy.Field()
    province = scrapy.Field()
    city = scrapy.Field()
    year = scrapy.Field()



