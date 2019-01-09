# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ImagePipelinesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    image_dir = scrapy.Field()
    image_paths = scrapy.Field()
    next_paths = scrapy.Field()
    print "yangna", image_urls, image_dir, image_paths, next_paths

class TaoTuLinkItem(scrapy.Item):
    item_link = scrapy.Field()
