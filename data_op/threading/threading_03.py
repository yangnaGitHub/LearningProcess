# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 18:00:23 2019

@author: yangna

@e-mail: ityangna0402@163.com
"""

import threading
from queue import Queue#队列

def job(mylist, myqueue):
    mylist = [val**2 for val in mylist]
    myqueue.put(mylist)

def multithreading():
    myqueue = Queue()
    threads = []
    data = [[1, 2, 3], [3, 4, 5], [4, 4, 4], [5, 5, 5]]
    for index in range(4):
        thread = threading.Thread(target=job, args=(data[index], myqueue))
        thread.start()#全部开始
        threads.append(thread)
    for thread in threads:
        thread.join()
    results = []
    for _ in range(4):
        results.append(myqueue.get())
    print(results)

if __name__ == '__main__':
    multithreading()