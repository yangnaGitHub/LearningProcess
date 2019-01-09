# -*- coding: utf-8 -*-
"""
Created on Tue Mar 07 12:44:22 2017

@author: natasha1_Yang
"""

#Python安装制定source:pip install -i https://pypi.tuna.tsinghua.edu.cn/simple xxxx
#TCP/IP四层协议 + OSI七层协议
#应用层(Http) + 传输层(Socket) + 互联网络层(路由器) + 网络接口层(交换机)
#应用层:HTTP(无连接+无状态) + FTP
#表示层:HTTPS
#传输层:TCP + UDP协议
#网络层:路由器 + IP协议
#数据链路层:交换机打包成数据帧
#Header很重要
#User-Agent:安卓手机
import urllib2
from collections import deque
from lxml import etree
import httplib
import hashlib
#from pybloom import BloomFilter

class CrawlBsf:
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
    #download_bf = BloomFilter(1024*1024*16, 0.01)
    
    dir_name = '.\\055_Crawl_Chapter_One\\'
    du_md5_file_name = dir_name + 'download.txt'#用来记录下载链接的MD5
    downloaded_urls = []#List可以用来防止重复
    
    cur_level = 0
    max_level = 5
    link_queue = deque()#每一层一个Queue,并不是为了广度,而是为了计层数
    child_link_queue = deque()
    
    def __init__(self, url):
        self.root_url = url
        self.link_queue.append(url)
        try:
            self.dumd5_file = open(self.du_md5_file_name, 'a+')
            self.downloaded_urls = self.dumd5_file.readlines()
        except IOError:
            print "File not found"
    
    def dequeUrl(self):
        try:
            url = self.link_queue.popleft()
            return url
        except IndexError:
            self.cur_level += 1
            if self.cur_level >= self.max_level:
                return None
            if len(self.child_link_queue) == 0:
                return None
            self.link_queue = self.child_link_queue
            self.child_link_queue = deque()
            return self.dequeUrl()
        
    def getpagecontent(self, cur_url):
        print "downloading %s" % (cur_url)
        try:
            req = urllib2.Request(cur_url, headers=self.request_headers)
            response = urllib2.urlopen(req)
            html_page = response.read()
            filename = cur_url[7:].replace("/", "_")
            fo = open("%s%s.html" % (self.dir_name, filename), "wb+")
            fo.write(html_page)
            fo.close()
        except urllib2.HTTPError, Arguments:
            print Arguments
            return
        except httplib.BadStatusLine:
            print "BadStatusLine"
            return
        except IOError:
            print 'IO Error at ' + filename
            return
        except Exception, Arguments:
            print Arguments
            return
        dumd5 = hashlib.md5(cur_url).hexdigest()
        #self.download_bf.add(dumd5)
        self.downloaded_urls.append(dumd5)
        self.dumd5_file.write(dumd5 + '\r\n')
        
        #html = etree.HTML(html_page.lower().decode("utf-8"))
        html = etree.HTML(html_page.lower())
        hrefs = html.xpath(u"//a")
        for href in hrefs:
            try:
                if "href" in href.attrib:
                    val = href.attrib["href"]
                    if val.find("javascript:") != -1:
                        continue
                    if val.startswith("http://") is False:
                        if val.startswith("/"):
                            val = 'http://www.mafengwo.cn' + val
                        else:
                            continue
                    if val[-1] == "/":
                        val = val[0:-1]
                    if hashlib.md5(val).hexdigest() not in self.downloaded_urls:#self.download_bf:
                        self.child_link_queue.append(val)
                    else:
                        print "Skip %s" % (val)
            except ValueError:
                continue
    
    def start_crawl(self):
        while True:
            url = self.dequeUrl()
            if url is None:
                break
            self.getpagecontent(url)
        self.dumd5_file.close() 

crawler = CrawlBsf("http://www.mafengwo.cn")
crawler.start_crawl()      