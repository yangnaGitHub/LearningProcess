# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 18:13:03 2019

@author: yangna

@e-mail: ityangna0402@163.com
"""

#Global Interpreter Lock (GIL),让Python一次性只能处理一个东西
#解释器被一个全局解释器锁保护着,确保任何时候都只有一个Python线程执行
#GIL最大的问题就是Python的多线程程序并不能利用多核CPU的优势
#一个使用了多个线程的计算密集型程序只会在一个单CPU上面运行
#解释器的C语言实现部分在完全并行执行时并不是线程安全的

import threading
from queue import Queue
import copy
import time

def job(mylist, myqueue):
    res = sum(mylist)
    myqueue.put(res)

def multithreading(mylist):
    myqueue = Queue()
    threads = []
    for index in range(4):
        thread = threading.Thread(target=job, args=(copy.copy(mylist), myqueue), name='T%i' % index)
        thread.start()
        threads.append(thread)
    [thread.join() for thread in threads]
    total = 0
    for _ in range(4):
        total += myqueue.get()
    print(total)

def normal(mylist):
    total = sum(mylist)
    print(total)

if __name__ == '__main__':
    mylist = list(range(1000000))
    s_t = time.time()
    normal(mylist*4)
    print('normal: ',time.time()-s_t)
    s_t = time.time()
    multithreading(mylist)
    print('multithreading: ', time.time()-s_t)