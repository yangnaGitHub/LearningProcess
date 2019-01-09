# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 18:12:23 2017

@author: natasha1_Yang
"""

from lxml import html
import urllib2

def parse_form(html_page):
    tree = html.fromstring(html_page)
    print tree
    data = {}
    for e in tree.cssselect("form input"):
        if e.get("name"):
            data[e.get("name")] = e.get("value")
    return data
    
url = "http://mail.163.com"

headers = {
    'host': "mail.163.com",
    'connection': "keep-alive",
    'cache-control': "no-cache",
    'accept-charset': "utf-8",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    'accept-language': "zh-CN,en-US;q=0.8,en;q=0.6",
    'postman-token': "dab3b5d5-2237-27e9-93bf-ad9ec0a451ac"
}

request = urllib2.Request(url, headers=headers)
response = urllib2.urlopen(request)
html_page = response.read()
data = parse_form(html_page)

print response.info().keys()