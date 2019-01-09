# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 16:10:49 2017

@author: natasha1_Yang
"""

import socket

class SocketClient:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        
        self.families = self.get_constants("AF_")
        self.types = self.get_constants("SOCK_")
        self.protocols = self.get_constants("IPPROTO_")
        
        #print >>sys.stderr, 'Family  :', self.families[sock.family]
        #print >>sys.stderr, 'Type    :', self.types[sock.type]
        #print >>sys.stderr, 'Protocol:', self.protocols[sock.proto]
        #print >>sys.stderr
#    for n in dir(socket):
#        if n.startswith("AF_"):
#            getattr(socket, n)
    def get_constants(self, prefix):
        return dict((getattr(socket, n), n)
                    for n in dir(socket)
                    if n.startswith(prefix)
                    )
    
    def send(self, message):
        try:
            #创建连接
            self.sock = socket.create_connection((self.server_ip, self.server_port))
            self.sock.sendall(message)
            data = self.sock.recv(1024)
            return data
        except socket.error as msg:
            print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            if msg[0] is 61:
                return None
        finally:
            if hasattr(self, "sock"):
                self.sock.close()