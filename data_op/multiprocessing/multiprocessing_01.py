# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 18:20:12 2019

@author: yangna

@e-mail: ityangna0402@163.com
"""

import multiprocessing as mp

#def job(first, second):
#    print(first+second)
#
##要在终端运行,不然不会有输出
#if __name__ == '__main__':
#    p1 = mp.Process(target=job, args=(1,2))
#    p1.start()
#    p1.join()

def job(myqueue):
    res = 0
    for index in range(1000):
        res += index + index**2 + index**3
    myqueue.put(res)

if __name__ == '__main__':
    myqueue = mp.Queue()
    #args的参数只有一个值的时候,后面需要加一个逗号,表示args是可迭代的,后面可能还有别的参数,不加逗号会出错
    p1 = mp.Process(target=job, args=(myqueue,))
    p2 = mp.Process(target=job, args=(myqueue,))
    
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    
    res1 = myqueue.get()
    res2 = myqueue.get()
    print(res1)
    print(res2)
    print(res1+res2)
    