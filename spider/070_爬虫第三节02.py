# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 17:14:37 2017

@author: natasha1_Yang
"""

import urllib2
import httplib
from lxml import etree
import threading
import time
#from MongoDb_070 import MongoUrlManager
from MongoRedisDb_070 import MongoRedisUrlManager
#from hdfs import *
#from hdfs.util import HdfsError
dir_name = '.\\070_Crawl_Chapter_Three\\'
request_headers = {
    'host': "www.mafengwo.cn",
    'accept-charset': "utf-8",
    'connection': "keep-alive",
    'cache-control': "no-cache",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36",
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    'accept-language': "zh-CN,en-US;q=0.8,en;q=0.6"
    }
def get_page_content(cur_url, depth):
    print "downloading %s at level %d" % (cur_url, depth)
    try:
        req = urllib2.Request(cur_url, headers=request_headers)
        response = urllib2.urlopen(req)
        html_page = response.read()
        filename = cur_url[7:].replace('/', '_')
        #Write page to local files system
        fo = open("%s%s.html" % (dir_name, filename), 'wb+')
        fo.write(html_page)
        fo.close()

        #with hdfs_client.write('/htmls/mfw/%s.html' % (filename)) as writer:
        #    writer.write(html_page)
        dbmanager.finishUrl(cur_url)
    except urllib2.HTTPError, Arguments:
        print Arguments
        return
    except httplib.BadStatusLine, Arguments:
        print Arguments
        return
    except IOError, Arguments:
        print Arguments
        return
    #except HdfsError, Arguments:
    #    print Arguments
    except Exception, Arguments:
        print Arguments
        return
    
    html = etree.HTML(html_page.lower())
    hrefs = html.xpath(u"//a")

    for href in hrefs:
        try:
            if 'href' in href.attrib:
                val = href.attrib['href']
                if val.find('javascript:') != -1:
                    continue
                if val.startswith('http://') is False:
                    if val.startswith('/'):
                        val = 'http://www.mafengwo.cn' + val
                    else:
                        continue
                if val[-1] == '/':
                    val = val[0:-1]
                dbmanager.enqueueUrl(val, 'new', depth + 1)
        except ValueError:
            continue

if __name__ == "__main__":
    max_num_thread = 5
    #dbmanager = MongoUrlManager(max_num_thread)
    dbmanager = MongoRedisUrlManager()
    dbmanager.enqueueUrl("http://www.mafengwo.cn", 'new', 0)
    start_time = time.time()
    is_root_page = True
    threads = []
    CRAWL_DELAY = 0.6
    #hdfs_client = InsecureClient('http://localhost:50070', user='ec2-user')
    while True:
        curtask = dbmanager.dequeueUrl()
        if curtask is None:
            for t in threads:
                t.join()
            break
        
        if is_root_page is True:
            #print curtask['_id'], curtask['depth']
            #get_page_content(curtask['_id'], curtask['depth'])
            print curtask['url'], curtask['depth']
            get_page_content(curtask['url'], curtask['depth'])
            is_root_page = False
        else:
            while True:
                for t in threads:
                    if not t.is_alive():
                        threads.remove(t)
                if len(threads) >= max_num_thread:
                    time.sleep(CRAWL_DELAY)
                    continue
                try:
                    #t = threading.Thread(target=get_page_content, name=None, args=(curtask['_id'], curtask['depth']))
                    t = threading.Thread(target=get_page_content, name=None, args=(curtask['url'], curtask['depth']))
                    threads.append(t)
                    t.setDaemon(True)
                    t.start()
                    time.sleep(CRAWL_DELAY)
                    break
                except Exception:
                    print "Error: unable to start thread"