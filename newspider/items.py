# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import re

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Identity, Join

class QuestionItem(scrapy.Item):
    # define the fields for your item here like:
    time = scrapy.Field(
        input_processor = lambda s: re.match(r'.*, (.*, \d*).*',s[0]).group(1)
    )
    url = scrapy.Field()
    keyword = scrapy.Field()
    question = scrapy.Field()
    name = scrapy.Field()
    univ = scrapy.Field()
    vote = scrapy.Field()
    confidence = scrapy.Field()
    comment = scrapy.Field()

class CfmItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    question = scrapy.Field()
    name = scrapy.Field()
    univ = scrapy.Field()
    answer = scrapy.Field()
    confidence = scrapy.Field()
    comment = scrapy.Field()


class MyItemLoader(ItemLoader):
    default_input_processor = MapCompose(lambda x: ' '.join(x.split()))
    default_output_processor = Join('')

