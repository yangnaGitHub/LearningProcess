# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 14:42:33 2017

@author: natasha1_Yang
"""

import urllib2
import re

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Charset': 'utf-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
    'Connection': 'keep-alive'
}

if __name__ == "__main__":
    item_url = "https://detail.tmall.com/item.htm?id=544500929933"
    try:
        req = urllib2.Request(item_url, headers=headers)
        response = urllib2.urlopen(req)
        content = response.read()
        with open("tmall_url.html", "w+") as f:
            f.write(content)
        
        tmall_links = re.findall('href=[\"\']{1}(//detail.tmall.com/item.htm[^>\"\'\s]+?)"', content)
        taobao_links = re.findall('href=[\"\']{1}(//detail.taobao.com/item.htm[^>\"\'\s]+?)"', content)
        
        for link in tmall_links:
            print link
        for link in taobao_links:
            print link
    except Exception, Arguments:
        print Arguments