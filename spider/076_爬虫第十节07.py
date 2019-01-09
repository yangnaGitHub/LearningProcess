# -*- coding: utf-8 -*-
"""
Created on Fri Jun 02 15:13:36 2017

@author: natasha1_Yang
"""

import urllib2
import re

from goose import Goose
from goose.text import StopWordsChinese

g = Goose({'stopwords_class': StopWordsChinese})

url = 'http://bbs.qyer.com/thread-2571140-1.html'

filename = "076_" + re.findall('/([^/]+)$', url)[0]

try:
    f = open(filename, 'rb')
    content = f.read()
    f.close()
except Exception:
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    content = response.read()
    
    f = open(filename, 'wb+')
    f.write(content)
    f.close()
    
article = g.extract(raw_html=content)
print article.cleaned_text