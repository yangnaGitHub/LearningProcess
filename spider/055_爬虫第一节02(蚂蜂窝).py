# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 15:36:43 2017

@author: natasha1_Yang
"""

import urllib2
import httplib
import hashlib
import re
import os

dirname = '.\\055_Crawl_Chapter_One\\MDD\\'
start_url = "http://www.mafengwo.cn/mdd/"  
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

all_city_list = []
city_ids = []
download_url = []

def download_city_notes(city_id):
    for index in xrange(1, 999):
        #/yj/10186/1-0-2.html游记的第二页
        url = "http://www.mafengwo.cn/yj/%s/1-0-%d.html" % (city_id, index)
        req = urllib2.Request(url, headers=request_headers)
        response = urllib2.urlopen(req)
        html_page = response.read()
        #/i/6526067.html==>href="/i/\d{7}.html
        city_notes = re.findall('href="/i/\d{7}.html', html_page)
        if len(city_notes) == 0:
            return
        for city_note in city_notes:
            try:
                city_url = "http://www.mafengwo.cn%s" % (city_note[6:])
                dumd5 = hashlib.md5(city_url).hexdigest()
                if dumd5 in download_url:
                    continue
                else:
                    download_url.append(dumd5)
                print 'download %s' % (city_url)
                req = urllib2.Request(city_url, headers=request_headers)
                response = urllib2.urlopen(req)
                html = response.read()
                filename = city_url[7:].replace('/', '_')
                fo = open("%s%s" % (dirname, filename), 'wb+')
                fo.write(html)
                fo.close()
            except Exception, Arguments:
                print Arguments
                continue
  
if __name__ == "__main__":
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    try:
        #目的地
        req = urllib2.Request(start_url, headers=request_headers)
        response = urllib2.urlopen(req)
        html_page = response.read()
        #利用正则表达式，找出所有的城市主页
        #/travel-scenic-spot/mafengwo/10065.html
        all_city_list = re.findall("/travel-scenic-spot/mafengwo/\d{5}.html", html_page)
        for city in all_city_list:
            city_ids.append(city[29:34])
            download_city_notes(city[29:34])
    except urllib2.HTTPError, Arguments:
        print Arguments
    except httplib.BadStatusLine:
        print "BadStatusLine"
    except Exception, Arguments:
        print Arguments
        