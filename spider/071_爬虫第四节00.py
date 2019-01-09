# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 14:59:32 2017

@author: natasha1_Yang
"""

import socket
import thread
import signal
import sys

class ServerSocket:
    def __init__(self, callback, host="localhost", port=20010):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.callback = callback
        try:
            self.s.bind((host, port))
        except socket.error as msg:
            print "Bind Failed, Error Code: " + str(msg[0]) + " Message " + msg[1]
            sys.exit()
        self.s.listen(10)
        
    #start_new_thread(function , args [ , kwargs ]) 
    
    def startlistening(self):
        while True:
            conn, addr = self.s.accept()
            print 'Connected with ' + addr[0] + ':' + str(addr[1])
            thread.start_new_thread(self.clientthread, (conn,))
    
    def clientthread(self, conn):
        #conn.send('Welcome to the server. Type something and hit enter\n')
        data = conn.recv(1024)#接收
        reply = self.callback(data)
        conn.sendall(reply)#发送
        conn.close()
    
    def start(self):
        thread.start_new_thread(self.startlistening, ())
    
    def close(self):
        self.s.close()
    
def msg_received(data):
    return "Ack"
    
def exit_signal_handler(signal, frame):
    pass

if __name__ == "__main__":
    server = ServerSocket(msg_received)
    server.start()
    signal.signal(signal.SIGINT, exit_signal_handler)
    signal.pause()
    server.close()
    sys.exit(1)