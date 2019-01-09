#两个级别访问的网络服务
#低级别的网络服务支持基本的Socket,可以访问底层操作系统Socket接口的全部方法
#高级别的网络服务模块SocketServer,提供了服务器中心
#应用程序通常通过"套接字"向网络发出请求或者应答网络请求,使主机间或者一台计算机上的进程间可以通讯
#创建套接字socket.socket([family[, type[, proto]]])
import socket
import sys
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()#获取本地主机名
print(host)
port = 9999
serversocket.bind((host, port))
serversocket.listen(5)#最大连接数
while True:
    clientsocket,addr = serversocket.accept()
    print("连接地址: %s" % str(addr))
    msg='welcome'+ "\r\n"
    clientsocket.send(msg.encode('utf-8'))
    clientsocket.close()
