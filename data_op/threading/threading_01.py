# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 17:41:20 2019

@author: yangna

@e-mail: ityangna0402@163.com
"""

import threading

#获取已激活的线程数
print(threading.active_count())

#查看所有线程信息
print(threading.enumerate())

#查看现在正在运行的线程
print(threading.current_thread())

#添加线程,threading.Thread()接收参数target代表这个线程要完成的任务
def thread_job():
    print('This is a thread of %s' % threading.current_thread())

if __name__ == '__main__':
    thread = threading.Thread(target=thread_job)
    thread.start()