# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 15:54:56 2017

@author: natasha1_Yang
"""

import urllib
import urllib2
#import glob
#import sqlite3
#import os
import cookielib

url = "https://dl.reg.163.com/gt"

headers = {
    'host': "https://dl.reg.163.com/gt",
    'connection': "keep-alive",
    'cache-control': "no-cache",
    'content-type': "application/x-www-form-urlencoded",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    'accept-language': "zh-CN,en-US;q=0.8,en;q=0.6",
}

data = {"un":"ityangna0402", "pkid":"CvViHzl", "pd":"mail163", "topURL":"", "nocache":1490863959026}
payload = urllib.urlencode(data)

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
request = urllib2.Request(url, payload, headers=headers)
response = opener.open(request)
print response.info()
print response.read()
for cookie in cj:
    print cookie