# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
class JDMongoPipelines(object):
    collection_name = "scrapy_items"
    #@staticmethod静态方法
    #有子类继承时,调用该类方法时,传入的类变量cls是子类
    #类方法,可以通过类来调用,也可以通过类的一个实例来调用
    @classmethod#类方法的第一个参数cls
    def from_crawler(cls, crawler):
        print "natasha + from_crawler"
        return cls(
            mongo_uri = crawler.settings.get("MONGO_URI"),
            mongo_db = crawler.settings.get("MONGO_DATABASE", "items")
        )
    
    def __init__(self, mongo_uri, mongo_db):
        print "natasha + __init__"
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
    
    def open_spider(self, spider):
        print "natasha + open_spider"
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
    
    def close_spider(self, spider):
        print "natasha + close_spider"
        self.client.close()
    
    def process_item(self, item, spider):
        print "natasha + process_item"
        self.db[self.collection_name].insert(dict(item))
        return item
