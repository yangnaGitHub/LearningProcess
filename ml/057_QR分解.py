# -*- coding: utf-8 -*-
"""
Created on Wed Mar 08 18:20:21 2017

@author: natasha1_Yang
"""

#把一个矩阵A通过HouseHolder变换做成上Hessenberg矩阵,然后通过Givens变换做QR分解
#Schmidt正交化
import numpy as np
import math

def is_same(a, b):
    n = len(a)
    for index in range(n):
        if math.fabs(a[index] - b[index]) > 1e-6:
            return False
    return True

if __name__ == "__main__":
    a = np.array([.65, .28, .07, .15, .67, .18, .12, .36, .52])
    dims = math.sqrt(len(a))
    a = a.reshape((int(dims), int(dims)))
    value, v = np.linalg.eig(a)#特征值, 特征向量
    
    times = 0
    while (0 == times) or (not is_same(np.diag(a), v)):#a的对角
        v = np.diag(a)
        q, r = np.linalg.qr(a)
        a = np.dot(r, q)
        times += 1
        print "对角阵: \n", v
        print "正交阵: \n", q
        print "三角阵: \n", r
        print "近似阵: \n", a
    print "次数: ", times, "近似值: ", np.diag(a)
    print "精确近似值: ", value
    