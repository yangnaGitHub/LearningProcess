# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 10:27:18 2019

@author: yangna

@e-mail: ityangna0402@163.com
"""

import multiprocessing as mp
import time

def job(v, num, l):
    l.acquire() #进程锁住
    for _ in range(5):
        time.sleep(0.1) 
        v.value += num #获取共享内存
        print(v.value)
    l.release() #进程释放

def multicore():
    l = mp.Lock() #定义一个进程锁
    v = mp.Value('i', 0) #定义共享内存
    p1 = mp.Process(target=job, args=(v,1,l)) #需要将lock传入
    p2 = mp.Process(target=job, args=(v,3,l)) 
    p1.start()
    p2.start()
    p1.join()
    p2.join()

if __name__ == '__main__':
    multicore()