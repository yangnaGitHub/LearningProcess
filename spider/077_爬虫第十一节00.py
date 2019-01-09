# -*- coding: utf-8 -*-
"""
Created on Fri Jun 02 16:28:26 2017

@author: natasha1_Yang
"""

import gzip
import re
import urllib2
import numpy as np
from StringIO import StringIO
from lxml.html import clean
import pylab
from sklearn.cluster import KMeans

request_headers = {
    'connection': "keep-alive",
    'cache-control': "no-cache",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36",
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    'accept-language': "zh-CN,en-US;q=0.8,en;q=0.6",
    'accept-charset ': 'utf-8'
}

url = 'http://news.sina.com.cn/c/gat/2017-03-13/doc-ifychhuq4322931.shtml'
#/[^/]+$ ==>/doc-ifychhuq4322931.shtml
#[]==>表示某个集合中的任意一个
filename = "077_" + re.findall('/([^/]+)$', url)[0]

try:
    f = open(filename, "rb")
    content = f.read()
    f.close()
except Exception:
    req = urllib2.Request(url, headers=request_headers)
    response = urllib2.urlopen(req)
    if response.info().get('Content-Encoding') == 'gzip':
        buf = StringIO(response.read())
        fzip = gzip.GzipFile(response.read())
        content = fzip.read()
    else:
        content = response.read()
    f = open(filename, "wb+")
    f.write(content)
    f.close()

cleaner = clean.Cleaner(style=True, scripts=True, comments=True, javascript=True, page_structure=False, safe_attrs_only=False)
content = cleaner.clean_html(content.decode('utf-8')).encode('utf-8')

reg = re.compile("<[^>]*>")
lines = content.split('\n')
cleaned_lines = []
counts = []
tags = []
ratios = []
for line in lines:
    tag = len(re.findall("<[^>]*>", line))
    line = reg.sub('', line)
    cleaned_lines.append(line)
    if tag == 0:
        tag = 1
        counts.append(len(line))
        tags.append(tag)
        ratios.append(len(line)/tag)

r = 2
ratio_smoth = [0, 0]
for k in range(r, len(ratios) - r):
    ratio_smoth.append(sum(ratios[k-r:k+r+1])/(2*r+1))#相邻的5个数求均值
feature = np.array(ratio_smoth).reshape(-1, 1)
kmeans = KMeans(2).fit(feature)
labels = kmeans.predict(feature)
centers = kmeans.cluster_centers_
mean = np.mean(ratio_smoth)
std = np.std(ratio_smoth)

clusters = {}
n = 0
for item in labels:
    if item in clusters:
        clusters[item].append(cleaned_lines[n])
    else:
        clusters[item] = [cleaned_lines[n]]
    n += 1
    
f = open('077_00_test.txt', "wb+")
index = 0
for i in centers:
    if i[0] > std:
        f.write('\n'.join(clusters[index]))
    index += 1
f.close()

pylab.plot(ratio_smoth, 'g-', linewidth=1.0)
pylab.savefig('077_word_count.png')
pylab.show()
