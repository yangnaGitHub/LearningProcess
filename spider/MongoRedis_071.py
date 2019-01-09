# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 16:36:54 2017

@author: natasha1_Yang
"""

import hashlib
from datetime import datetime
from datetime import timedelta
import redis
from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING

class MongoRedisUrlManager:
    def __init__(self, server_ip="localhost", client=None, expires=timedelta(days=30)):
        self.client = MongoClient(server_ip, 27017)
        self.redis_client = redis.StrictRedis(host=server_ip, port=6379, db=0, password="natasha3021")
        self.db = self.client.spider
        if self.db.mfw_redis.count() is 0:
            self.db.mfw_redis.create_index([("status", ASCENDING), ("pr", DESCENDING)])
    
    def dequeueUrl(self):
        record = self.db.mfw_redis.find_one_and_update(
            {"status": "new"},
            {"$set": {"status": "downloading"}},
            upsert=False, 
            sort=[('pr', DESCENDING)],#按照降序排列
            returnNewDocument= False
            )
        if record:
            return record
        else:
            return None
    
    def enqueueUrl(self, url, status, depth):
        num = self.redis_client.get(url)
        if num is not None:
            self.redis_client.set(url, int(num) + 1)
            return
        self.redis_client.set(url, 1)
        self.db.mfw_redis.insert({
            "_id": hashlib.md5(url).hexdigest(),
            "url": url,
            "status": status,
            "queue_time": datetime.utcnow(),
            "depth": depth,
            "pr": 0
            })
       
    def finishUrl(self, url):
        record = {"status": "done", "done_time": datetime.utcnow()}
        self.db.mfw_redis.update({"_id": hashlib.md5(url).hexdigest()}, {"$set": record}, upsert=False)
    
    def set_url_links(self, url, links):
        self.db.urlpr.insert({
            "_id": hashlib.md5(url).hexdigest(),
            "url": url,
            "links": links
            })
    
    def clear(self):
        self.db.mfw_redis.drop()