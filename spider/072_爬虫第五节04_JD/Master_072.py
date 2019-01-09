# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 17:04:09 2017

@author: natasha1_Yang
"""

import hashlib
from Socket_Server_072 import ServerSocket
import Protocol_Constants_072 as pc
import time
from pymongo import MongoClient
#import signal
import thread
import networkx as nx
import json
#import sys

constants = {
    "reorder_period": 1200,#20mins
    "connection_lost_period": 30#30s
    }
    
class CrawlMaster:
    clients = {}
    server_status = pc.STATUS_RUNNING
    last_reorder_time = time.time()
    is_reordering = False
    
    def __init__(self, mongo_client = None, mongo_host="localhost"):
        mongo_client = MongoClient(mongo_host, 27017)
        self.db = mongo_client.spider
        self.server = ServerSocket(self.on_message)
        self.server.start()
    
    def on_message(self, msg):
        request = json.loads(msg)
        client_type = request[pc.MSG_TYPE]
        client_state = {}
        response = {}
        response[pc.SERVER_STATUS] = self.server_status
        if client_type == pc.REGISTER:
            client_id = self.get_free_id()
            client_state["status"] = pc.STATUS_RUNNING
            client_state["time"] = time.time()
            self.clients[client_id] = client_state
            return client_id
        elif client_type == pc.UNREGISTER:
            client_id = request.get(pc.CLIENT_ID)
            del self.clients[client_id]
            return json.dumps(response)
        
        client_id = request.get(pc.CLIENT_ID)
        if client_id is None:
            response[pc.ERROR] = pc.ERR_NOT_FOUND
            return json.dumps(response)
        if client_type == pc.HEARTBEAT:
            if self.server_status is not self.clients[client_id]["status"]:
                if self.server_status == pc.STATUS_RUNNING:
                    response[pc.ACTION_REQUIRED] = pc.RESUME_REQUIRED
                elif self.server_status == pc.STATUS_PAUSED:
                    response[pc.ACTION_REQUIRED] = pc.PAUSE_REQUIRED
                elif self.server_status == pc.STATUS_SHUTDOWN:
                    response[pc.ACTION_REQUIRED] = pc.SHUTDOWN_REQUIRED
                return json.dumps(response)
        else:
            client_state["status"] = client_type
            client_state["time"] = time.time()
            self.clients[client_id] = client_state
        return json.dumps(response)
    
    def get_free_id(self):
        index = 0
        for key in self.clients:
            if index < int(key):
                break
            index += 1
        return str(index)
    
    def reorder_queue(self):
        g = nx.DiGraph()
        cursor = self.db.urlpr.find()
        for site in cursor:
            url = site["url"]
            links = site["links"]
            for link in links:
                g.add_edge(url, link)
        pageranks = nx.pagerank(g, 0.9)
        for url, pr in pageranks.iteritems():
            print "updating %s pr: %f" % (url, pr)
            record = {'pr': pr}
            self.db.mfw_redis.update_one({"_id": hashlib.md5(url).hexdigest()}, {"$set": record}, upsert=False)
    
    def periodocal_check(self):
        clients_status_ok = True
        #重排
        if self.is_reordering is False and time.time() - self.last_reorder_time > constants["reorder_period"]:
            self.server_status = pc.STATUS_PAUSED
            self.is_reordering = True
        #client的ID和状态
        for cid, state in self.clients.iteritems():
            if time.time() - state["time"] > constants["connection_lost_period"]:
                self.clients[cid]["status"] = pc.STATUS_CONNECTION_LOST
                continue
            if state["status"] != self.server_status:
                clients_status_ok = False
                break
        
        if clients_status_ok and self.server_status == pc.STATUS_PAUSED and self.is_reordering:
            self.reorder_queue()
            self.last_reorder_time = time.time()
            self.is_reordering = False
            self.server_status = pc.STATUS_RUNNING

#def exit_signal_handler(signal, frame):
#    crawl_master.server.close()
#    sys.exit(1)

if __name__ == "__main__":
    crawl_master = CrawlMaster()
    thread.start_new_thread(crawl_master.periodocal_check, ())
    #signal.signal(signal.SIGINT, exit_signal_handler)
    #signal.pause()