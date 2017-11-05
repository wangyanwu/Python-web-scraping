# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XpathiimageItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    """
    siteURL:详情页地址
    detailURL：图片地址
    title：番号
    actress：演员
    """
    siteURL=scrapy.Field()
    detailURL=scrapy.Field()
    title=scrapy.Field()
    actress=scrapy.Field()
    pass
