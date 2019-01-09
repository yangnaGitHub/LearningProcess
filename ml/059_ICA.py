# -*- coding: utf-8 -*-
"""
Created on Thu Mar 09 16:41:41 2017

@author: natasha1_Yang
"""

import math
import numpy as np

def mix(A, s1, s2):
    mix = np.dot(A, np.array([s1, s2]))
    for index in xrange(len(mix[0])):
        mix[0][index] = mix[0][index] + mix[1][index]
    return mix
    
def ica(x):
    m = len(x)
    n = len(x[0])
    #n * n
    w = [[0.0]*n for t in range(n)]
    iw = [[0.0]*n for t in range(n)]
    w1 = [[0.0]*n for t in range(n)]
    for index in range(n):
        w[index][index] = 1
    alpha = 0.001
    #shuffle(x)
    for time in range(200):
        for mindex in range(m):
            for nindex in range(n):
                temp = np.dot(w[nindex], x[mindex])
                temp = 1 - 2 * logistic(temp)
                w1[nindex] = n_multiply(temp, x[mindex])
            
    
def decode(w, x):
    
def show_data(ps1, ps2):
    

if __name__ == "__main__":
    s1 = [math.sin(float(x)/20) for x in range(0, 1000, 1)]
    s2 = [float(x)/50 for x in range(0, 50, 1)] * 20
    #原始的源信号是N维的,混合信号也是N维的,混合矩阵A和解混矩阵W都是N*N维
    #混合矩阵A必须是N*N维,才能使得n维的原始信号乘上A后可以得到个n维的混合信号
    A = [[.6, .4], [.45, .55]]
    x = mix(A, s1, s2)#s1,s2线性加权得到输入数据
    #去均值
    x_mean = np.mean(x)
    for mindex in xrange(x.shape[0]):
        for nindex in xrange(x.shape[1]):
            x[mindex][nindex] = x[mindex][nindex] - x_mean
    #ICA
    w = ica(x)
    #Decode
    [ps1, ps2] = decode(w, x)
    show_data(ps1, ps2)