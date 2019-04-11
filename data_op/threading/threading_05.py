# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 18:15:53 2019

@author: yangna

@e-mail: ityangna0402@163.com
"""

import threading
import time

def job1_nl():
    global A
    for index in range(10):
        A += 1
        time.sleep(0.01)
        print('job1', A)

def job2_nl():
    global A
    for index in range(10):
        A += 10
        print('job2', A)

def job1():
    global A, lock
    lock.acquire()
    for i in range(10):
        A += 1
        print('job1', A)
    lock.release()

def job2():
    global A, lock
    lock.acquire()
    for i in range(10):
        A += 10
        print('job2', A)
    lock.release()

if __name__ == '__main__':
    #在每个线程执行运算修改共享内存之前,执行lock.acquire()将共享内存上锁
    #确保当前线程执行时,内存不会被其他线程访问,执行运算完毕后,使用lock.release()将锁打开
    lock = threading.Lock()
    A = 0
    t1 = threading.Thread(target=job1)
    t2 = threading.Thread(target=job2)
    t1.start()
    t2.start()
    t1.join()
    t2.join()