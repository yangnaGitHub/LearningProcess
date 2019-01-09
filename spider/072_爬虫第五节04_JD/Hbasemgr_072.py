# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 16:22:22 2017

@author: natasha1_Yang
"""

import happybase#Hbasemgr_072

class HBaseManager:
    config = {
        "BATCH_SIZE":1000
    }
    
    def __init__(self, host="localhost", namespace="crawler", table_name="html"):
        self.conn = happybase.Connection(host = host,
            table_prefix = namespace,
            table_prefix_separator=":")
        self.conn.open()
        self.table = self.conn.table(table_name)
        self.batch = self.table.batch(batch_size = self.config["BATCH_SIZE"])
        
    def append_page_content(self, url, family, col, content):
        self.table.put(url, {"%s:%s" % (family, col) : content})
        
    def append_page_content(self, url, batchdata):
        self.table.put(url, batchdata)
    
    def close(self):
        self.conn.close()