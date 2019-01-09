# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 09:52:06 2017

@author: natasha1_Yang
"""

import urllib2, httplib, socket

class BindableHTTPConnection(httplib.HTTPConnection):
    def connect(self):
        """Connect to the host and port specified in __init__"""
        print "connect"
        self.sock = socket.socket()
        self.sock.bind((self.source_ip, 0))
        if isinstance(self.timeout, float):
            self.sock.settimeout(self.timeout)
        self.sock.connect((self.host, self.port))
    
def BindableHTTPConnectionFactory(source_ip):
    def _get(host, port=None, strict=None, timeout=0):
        print "_get"
        bhc = BindableHTTPConnection(host, port=port, strict=strict, timeout=timeout)
        bhc.source_ip = source_ip
        return bhc
    return _get

class BindableHTTPHandler(urllib2.HTTPHandler):
    def http_open(self, req):
        print "http_open"
        return self.do_open(BindableHTTPConnectionFactory("127.0.0.1"), req)

opener = urllib2.build_opener(BindableHTTPHandler)
print "start"
opener.open("http://google.com/").read()