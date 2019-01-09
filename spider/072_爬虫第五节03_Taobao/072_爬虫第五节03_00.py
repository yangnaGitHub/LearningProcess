# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 10:29:18 2017

@author: natasha1_Yang
"""

import hashlib
from collections import deque
from selenium import webdriver
import re
from lxml import etree
import time
from pybloom import BloomFilter
import sys

headers = {
    "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "accept-language":"zh-CN,zh;q=0.8",
    "user-agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    'Connection': 'keep-alive',
    'Accept-Charset': 'utf-8'
}

for key, value in headers.iteritems():
    webdriver.DesiredCapabilities.PHANTOMJS["phantomjs.page.customHeaders.{}".format(key)] = value

webdriver.DesiredCapabilities.PHANTOMJS["phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"

start_url = "https://detail.tmall.com/item.htm?id=544500929933"
#driver = webdriver.PhantomJS(service_args=["--load-image=false"])
driver = webdriver.PhantomJS()
driver.set_window_size(1280, 2400)

download_bf = BloomFilter(1024 * 1024 * 14, 0.01)
cur_queue = deque()

def enqueueUrl(url):
    try:
        md5v = hashlib.md5(url).hexdigest()
        if md5v not in download_bf:
            cur_queue.append(url)
            download_bf.add(md5v)
    except ValueError:
        pass

def dequeueUrl():
    return cur_queue.popleft()

def crawl(url):
    print "crawling " + url
    driver.get(url)
    
    time.sleep(5)
    
    content = driver.page_source
    with open("tmall_cat.html", "w+") as f:
        f.write(content.encode('utf-8'))
    
    #href="//detail.tmall.com/item.htm?spm=a220o.1000855.1998025129.1.epsBRj&abtest=_AB-LR32-PR32&pvid=9da7780c-df6e-43ed-8d00-3beecda49c2d&pos=1&abbucket=_AB-M32_B19&acm=03054.1003.1.1539344&id=544894702615&scm=1007.12144.78696.23864_23864
    #[^>\"\'s]+?匹配任意不为 > " ' 空格 制表符 的字符
    tmall_links = re.findall('href=[\"\']{1}(//detail.tmall.com/item.htm[^>\"\'s]+?)"', content)
    taobao_links = re.findall('href=[\"\']{1}(//detail.taobao.com/item.htm[^>\"\'s]+?)"', content)
    etr = etree.HTML(content)
    item_price_list = etr.xpath('//span[@class="tm-price"]')
    if len(item_price_list) == 0:
        real_price = 0
    elif len(item_price_list) == 1:
        real_price = item_price_list[0].text
    else:
        real_price = etr.xpath('//dl[contains(@class, "tm-promo-cur")]//span[@class="tm-price"]')
    
    title = etr.xpath('//*[@class="tb-detail-hd"]/h1')[0].text
    title = title.strip()
    
    print "+++++++++++++++++++"
    print title
    print real_price[0].text
    print "+++++++++++++++++++"
    
    for href in tmall_links + taobao_links:
        href = "https:" + href
        enqueueUrl(href)
    try:
        crawl(dequeueUrl())
    except IndexError:
        sys.exit(0)
    
if __name__ == "__main__":
    crawl(start_url)
    driver.quit()