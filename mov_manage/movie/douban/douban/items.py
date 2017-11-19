# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from movie.models import Detail , Comments
from scrapy_djangoitem import DjangoItem


class DoubanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class DetailItem(DjangoItem):
    django_model = Detail

class CommentsItem(DjangoItem):
    django_model = Comments
