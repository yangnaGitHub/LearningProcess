# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 18:18:44 2017

@author: natasha1_Yang
"""

#import subprocess
import threading
import time
from datetime import datetime
from datetime import date
from MongoRedis_072 import MongoRedisUrlManager
import socket
#提供2个Function
#get_constants根据前缀获取定义的常量
#send创建一个连接发送所有的数据并接收数据并返回数据
from Socket_Client_072 import SocketClient
import Protocol_Constants_072 as pc
import json
from Hbasemgr_072 import HBaseManager
from selenium import webdriver
import re
from lxml import etree
import os

#import py_compile
#py_compile.compile("")
#python -m py_compile file.py
#python -O -m py_compile file.py

dir_name = '.\\jd_html\\'

#重写json使得可以序列化时间数据
class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)
    
headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Charset':'utf-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
    'Connection': 'keep-alive'
    }
    
constants = {
    'MAX_PAGE_TRIED': 2,
    'HB_PERIOD': 5,
    'MAX_SIZE_THREADPOOL': 3,
    'CRAWL_DELAY': 2
}

def get_page_content(cur_url, depth, driver):
    print "downloading %s at level %d" % (cur_url, depth)
    
    price = ""
    rating = ""
    content = ""
    item_name = ""
    iid_match_obj = re_compiled_obj.search(cur_url)
    #http://www.robot-china.com/news/201410/31/15241.html
    try:
        driver.get(cur_url)
        content = driver.page_source
        if iid_match_obj is not None:
            item_id = cur_url[iid_match_obj.start():iid_match_obj.end()]
            tree = etree.HTML(content)
            if len(tree.xpath(u"//div[@id='name']/h1")) > 0:
                item_name = tree.xpath(u"//div[@id='name']/h1")[0].text.strip()
            elif len(tree.xpath(u"//*[@class='sku-name']")) > 0:
                item_name = tree.xpath(u"//*[@class='sku-name']")[0].text.strip()
            else:
                print cur_url + "==> name not found!!!"
            
            price_node = tree.xpath(u"//*[contains(@class, '%s')]" % ("J-p-%s" % (item_id)))
            if len(price_node) > 0:
                price = price_node[0].text
            else:
                print cur_url + "==> price not found!!!"
            
            if len(tree.xpath(u"//*[@class='percent-con']")) > 0:
                rating = tree.xpath(u"//*[@class='percent-con']")[0].text
            elif len(tree.xpath(u"//*[@class='rate']")) > 0:
                rating = tree.xpath(u"//*[@class='rate']/strong")[0].text
            else:
                print cur_url + "==> rating not found!!!"
        
        print "++++++++++++++++++++++++"
        print item_name
        print rating
        print price
        print "++++++++++++++++++++++++"
        
        with open("%s%s.html" % (dir_name, item_id), "wb+") as f:
            f.write(content)
        
    except Exception, Arguments:
        print Arguments
        return
    
    dbmanager.finishUrl(cur_url)
    
    items = re.findall("//item.jd.com/\d{7}.html", content)
    lists = re.findall("//list.jd.com/list.html\?cat=\d{3,5},\d{3,5},\d{3,5}", content)
    links = []
    
    for href in items + lists:
        try:
            href = "https:" + href
            links.append(href)
            dbmanager.enqueueUrl(href, "new", depth + 1)
        except ValueError:
            continue
    dbmanager.set_url_links(cur_url, links)

def get_web_driver():
    if len(webdrivers) == 0:
        for index in range(0, constants["MAX_SIZE_THREADPOOL"]):
            driver = webdriver.PhantomJS()
            driver.set_window_size(1280, 2400)
            webdrivers[driver] = False
    for dr in webdrivers:
        if webdrivers[dr] is False:
            return dr
    
def heartbeat():
    global server_status, run_heartbeat, client_id
    skip_wait = False
    while run_heartbeat:
        if skip_wait is False:
            time.sleep(constants["HB_PERIOD"])
        else:
            skip_wait = False
        try:
            hb_request = {}
            hb_request[pc.MSG_TYPE] = pc.HEARTBEAT
            hb_request[pc.CLIENT_ID] = client_id
            hb_response_data = socket_client.send(json.dumps(hb_request))
            
            if hb_response_data is None:
                server_status = pc.STATUS_CONNECTION_LOST
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
    if os.path.exists(dir_name):
        os.mkdir(dir_name)
    
    for key, value in headers.iteritems():
        webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.{}'.format(key)] = value
    webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.settings.userAgent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'

    dbmanager = MongoRedisUrlManager()
    
    start_time = time.time()
    threads = []
    webdrivers = []
    
    socket_client = SocketClient('localhost', 13140)
    register_request = {}
    register_request[pc.MSG_TYPE] = pc.REGISTER
    client_id = socket_client.send(json.dumps(register_request))
    
    run_heartbeat = True
    server_status = pc.STATUS_RUNNING
    
    re_compiled_obj = re.compile('\d{7}')
    hbase = HBaseManager(host="localhost")
    
    thread_pool_drivers = {}
    
    try:
        t = threading.Thread(target=heartbeat, name=None)
        t.setDaemon(True)
        t.start()
    except Exception:
        print "Error: unable to start thread"
    
    curtask = dbmanager.dequeueUrl()
    if curtask is None:
        dbmanager.enqueueUrl('https://www.jd.com', 'new', 0 )
        is_root_page = True
    else:
        is_root_page = False
    while True:
        if server_status == pc.STATUS_PAUSED or server_status == pc.STATUS_CONNECTION_LOST:
            time.sleep(constants["HB_PERIOD"])
            #continue
        if server_status == pc.SHUTDOWN:
            run_heartbeat = False
            for t in threads:
                t.join()
        curtask = dbmanager.dequeueUrl()
        #print 'cur task is: ' + json.dumps(curtask)
        #json不能很好的序列化时间数据,要重写json
        if curtask is None:
            time.sleep(constants["HB_PERIOD"])
            continue
        if is_root_page is True:
            driver = get_web_driver()
            get_page_content(curtask['url'], curtask['depth'], driver)
            is_root_page = False
        else:
            while True:
                for t in threads:
                    if not t.is_alive():
                        driver = threads[t]
                        webdrivers[driver] = False
                        del threads[t]
                if len(threads) >= constants["MAX_SIZE_THREADPOOL"]:
                    time.sleep(constants["CRAWL_DELAY"])
                    continue
                try:
                    t = threading.Thread(target=get_page_content, name=None, args=(curtask['url'], curtask['depth']))
                    threads[t] = get_web_driver()
                    t.setDaemon(True)
                    t.start()
                    time.sleep(constants["CRAWL_DELAY"])
                    break
                except Exception, Arguments:
                    time.sleep(constants['CRAWL_DELAY'])
                    print "Error: unable to start thread"
                    print Arguments
    shutdown_request = {}
    shutdown_request[pc.MSG_TYPE] = pc.SHUTDOWN
    shutdown_request[pc.CLIENT_ID] = client_id
    socket_client.send(json.dumps(shutdown_request))
    for dr in webdrivers:
        dr.close()
        dr.quit()
    # kill all phantomjs
    #subprocess.call('pgrep phantomjs | xargs kill')