# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 10:09:04 2019

@author: yangna

@e-mail: ityangna0402@163.com
"""

import multiprocessing as mp

def job(x_val):
    return x_val*x_val

def multicore():
    pool = mp.Pool(processes=2)#定义一个Pool,自定义需要的核数量
    #map()中需要放入函数和需要迭代运算的值,然后它会自动分配给CPU核
    res = pool.map(job, range(10))
    print(res)#[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
    #只能传递一个值,只会放入一个核进行运算,传入值时要注意是可迭代的
    #需要用get()方法获取返回值
    res = pool.apply_async(job, (2,))#还有可以返回结果的方式,那就是apply_async()
    print(res.get())#4
    multi_res =[pool.apply_async(job, (index,)) for index in range(10)]
    print([res.get() for res in multi_res])#[0, 1, 4, 9, 16, 25, 36, 49, 64, 81

if __name__ == '__main__':
    multicore()
#map()放入迭代参数返回多个结果
#apply_async()只能放入一组参数,并返回一个结果,如果想得到map()的效果需要通过迭代