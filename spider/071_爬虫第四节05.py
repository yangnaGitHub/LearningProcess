# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 18:18:44 2017

@author: natasha1_Yang
"""

import urllib2
import httplib
from hdfs import HdfsError
from lxml import etree
import threading
import time
from MongoRedis_071 import MongoRedisUrlManager
import argparse
import socket

from datetime import date
from datetime import datetime
#提供2个Function
#get_constants根据前缀获取定义的常量
#send创建一个连接发送所有的数据并接收数据并返回数据
from Socket_Client_071 import SocketClient
import Protocol_Constants_071 as pc
import json
import os

class arguments:
    pass

#重写json使得可以序列化时间数据
class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)

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

dir_name = '.\\071_Crawl_Chapter_Four\\'

def get_page_content(cur_url, depth):
    print "downloading %s at level %d" % (cur_url, depth)
    links = {}
    try:
        req = urllib2.Request(cur_url, headers=request_headers)
        response = urllib2.urlopen(req)
        html_page = response.read()
        filename = cur_url[7:].replace('/', '_')

        #Write page to local files system
        fo = open("%s%s.html" % (dir_name, filename), 'wb+')
        fo.write(html_page)
        fo.close()

        #Write to HDFS
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
    except HdfsError, Arguments:
        print Arguments
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
                links.append(val)#某个网址下面所有的网址
                dbmanager.enqueueUrl(val, 'new', depth+1)
        except ValueError:
            continue

    dbmanager.set_url_links(cur_url, links)
    
def heartbeat():
    global server_status, run_heartbeat, client_id
    skip_wait = False
    while run_heartbeat:
        if skip_wait is False:
            time.sleep(hb_period)
        else:
            skip_wait = False
        try:
            hb_request = {}
            hb_request[pc.MSG_TYPE] = pc.HEARTBEAT
            hb_request[pc.CLIENT_ID] = client_id
            hb_response_data = socket_client.send(json.dumps(hb_request))
            
            if hb_response_data is None:
                continue
            response = json.loads(hb_response_data)
            err = response.get(pc.ERROR)
            if err is not None:
                if err == pc.ERR_NOT_FOUND:
                    register_request = {}
                    register_request[pc.MSG_TYPE] = pc.REGISTER
                    client_id = socket_client.send(json.dumps(register_request))
                    skip_wait = True
                    heartbeat()
                    return
                return
            
            action = response.get(pc.ACTION_REQUIRED)
            if action is not None:
                action_request = {}
                if action == pc.PAUSE_REQUIRED:
                    server_status = pc.PAUSED
                    action_request[pc.MSG_TYPE] = pc.PAUSED
                elif action == pc.RESUME_REQUIRED:
                    server_status = pc.RESUMED
                    action_request[pc.MSG_TYPE] = pc.RESUMED
                elif action == pc.SHUTDOWN_REQUIRED:
                    server_status = pc.SHUTDOWN
                    return
                action_request[pc.CLIENT_ID] = client_id
                socket_client.send(json.dumps(action_request))
            else:
                server_status = response[pc.SERVER_STATUS]
        except socket.error as msg:
            print 'Send Data Error. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            server_status = pc.STATUS_CONNECTION_LOST

if __name__ == "__main__":
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
        
    args = arguments()
    parser = argparse.ArgumentParser(prog="CrawlerClient", description="Start a crawal client")
    parser.add_argument("-S", "--host-all", type=str, nargs=1, help="Host server for all services")
    parser.add_argument("-s", "--host", type=str, nargs=1, help="Crawler host server address, default is localhost")
    parser.add_argument("-p", "--host-port", type=int, nargs=1, help="Crawler host server port number, default is 20100")
    parser.add_argument("-m", "--mongo", type=str, nargs=1, help="Mongo server address, default is localhost")
    parser.add_argument("-n", "--mongo-port", type=int, nargs=1, help="Mongo port number, default is 27017")
    parser.add_argument("-r", "--redis", type=str, nargs=1, help="Redis server address, default is localhost")
    parser.add_argument("-x", "--redis-port", type=int, nargs=1, help="Redis port number, default is 6379")
    parser.parse_args(namespace=args)

    if args.host_all is not None:
        args.host = args.mongo = args.redis = args.host_all
        
    if args.host is None:
        args.host = "localhost"
        
    if args.mongo is None:
        args.mongo = "localhost"
        
    if args.redis is None:
        args.redis = "localhost"
        
    if args.host_port is None:
        args.host_port = 9999
    
    if args.mongo_port is None:
        args.mongo_port = 27017
    
    if args.redis_port is None:
        args.redis_port = 6379
    
    max_num_thread = 5
    dbmanager = MongoRedisUrlManager()
    dbmanager.enqueueUrl('http://www.mafengwo.cn', 'new', 0 )
    
    start_time = time.time()
    is_root_page = True
    threads = []
    CRAWL_DELAY = 1
    
    socket_client = SocketClient('localhost', 13140)
    register_request = {}
    register_request[pc.MSG_TYPE] = pc.REGISTER
    client_id = socket_client.send(json.dumps(register_request))
    
    hb_period = 5
    run_heartbeat = True
    server_status = pc.STATUS_RUNNING
    
    try:
        t = threading.Thread(target=heartbeat, name=None)
        t.setDaemon(True)
        t.start()
    except Exception:
        print "Error: unable to start thread"
    
    while True:
        if server_status == pc.STATUS_PAUSED:
            time.sleep(hb_period)
            #continue
        if server_status == pc.SHUTDOWN:
            run_heartbeat = False
            for t in threads:
                t.join()
        curtask = dbmanager.dequeueUrl()
        #print 'cur task is: ' + json.dumps(curtask)
        #json不能很好的序列化时间数据,要重写json
        if curtask is None:
            time.sleep(hb_period)
            continue
        if is_root_page is True:
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
                    t = threading.Thread(target=get_page_content, name=None, args=(curtask['url'], curtask['depth']))
                    threads.append(t)
                    t.setDaemon(True)
                    t.start()
                    time.sleep(CRAWL_DELAY)
                    break
                except Exception:
                    print "Error: unable to start thread"
    shutdown_request = {}
    shutdown_request[pc.MSG_TYPE] = pc.SHUTDOWN
    shutdown_request[pc.CLIENT_ID] = client_id
    socket_client.send(json.dumps(shutdown_request))