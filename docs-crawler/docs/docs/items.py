# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ApiItem(scrapy.Item):
    code = scrapy.Field()
    function_name = scrapy.Field()
    args = scrapy.Field()
    kwargs = scrapy.Field()
