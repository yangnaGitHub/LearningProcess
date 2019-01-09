# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 16:04:36 2017

@author: natasha1_Yang
"""

import urllib2#下载
import json#内容解析
from bs4 import BeautifulSoup#内容选择

url_format = "http://www.autohome.com.cn/grade/carhtml/%s.html"

html_doc = ""
start_char = "A"
RequestHeaders = {}
for i in range(ord('A'), ord('Z')):
    req = urllib2.Request(url_format % (chr(i)), headers=RequestHeaders)
    #headers请求的核心
    #Cookie:用来标识用户,再次发起请求加上Cookie传给服务器就知道你是谁
    #postman批量拿到Header
    response = urllib2.urlopen(req)
    page = response.read()
    html_doc += page
    
    fo = open("autohome.html", "wb+")
    fo.write(html_doc)
    fo.close()
    
soup = BeautifulSoup(fo, "html.parser")
model_file = open("models.txt", "wb")
for model in soup.find_all("h4"):
    try:
        if model.string is not None:
            mode_file.write("%s\r\n" % (model.string.encode("utf-8")))
    except ValueError:
        continue