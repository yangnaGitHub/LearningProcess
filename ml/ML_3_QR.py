# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 11:17:05 2016

@author: natasha1_Yang
"""
import numpy as np
import math

def is_same(a, b):
    n = len(a)
    for i in range(n):
        if math.fabs(a[i] - b[i]) > 1e-6:
            return False
    return True
    
if __name__ == "__main__":
    a = np.array([.65, .28, .07, .15, .67, .18, .12, .36, .52])
    n = math.sqrt(len(a))
    a = a.reshape(n, n)
    value, v = np.linalg.eig(a)#矩阵a的特征值和特征向量
    print a, value, v
    times = 0
    while(times == 0) or (not is_same(np.diag(a), v)):
        v = np.diag(a)
        q, r = np.linalg.qr(a)
        a = np.dot(r, q)
        times += 1
        print "正交阵: \n", q
        print "三角阵: \n", r
        print "近似阵: \n", a
    print "次数: ", times, "近似值: ", np.diag(a)
    print "精确特征值: ", value