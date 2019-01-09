# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 16:16:34 2017

@author: natasha1_Yang
"""

from pymongo import MongoClient
from datetime import datetime
from datetime import timedelta
from pymongo import errors

class MongoUrlManager:
    SERVER_IP = "localhost"
    
    def __init__(self, client=None, expires=timedelta(days=30)):
        self.client = MongoClient(self.SERVER_IP, 27017)#if client is None else client
        self.db = self.client.spider
        
    def dequeueUrl(self):
        record = self.db.mfw.find_one_and_update(
            {'status': 'new'},
            {'$set': {'status': 'downloading'}},
            {'upsert': False, 'returnNewDocument': False}
            )
        if record:
            return record
        else:
            return None
    
    def enqueueUrl(self, url, status, depth):
        try:
            record = {'status': status, 'queue_time': datetime.utcnow(), 'depth': depth}
            self.db.mfw.insert({'_id': url})#无法插入整条数据,只有通过更新的方法
            self.db.mfw.update({'_id': url}, {'$set': record}, upsert=False)
        except errors.DuplicateKeyError:
            print "DuplicateKeyError %s" % (url)
    
    def finishUrl(self, url):
        record = {'status': 'done', 'done_time': datetime.utcnow()}
        self.db.mfw.update({'_id': url}, {'$set': record}, upsert=False)
        
    def clear(self):
        self.db.mfw.drop()