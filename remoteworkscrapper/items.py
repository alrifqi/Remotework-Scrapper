# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Field, Item


class RemoteworkscrapperItem(Item):
    title = Field()
    desc = Field()
    url = Field()
    company = Field()
    source = Field()
