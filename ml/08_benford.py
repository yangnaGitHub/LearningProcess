# -*- coding: utf-8 -*-

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from time import time
from scipy.special import factorial
import math

mpl.rcParams['axes.unicode_minus'] = False
mpl.rcParams['font.sans-serif'] = 'SimHei'

def top1(number, a):
    number /= a
    while number >= 10:
        number /= 10
        a *= 10
    return number, a
    
def top2(number, n):
    while number >= n:
        number /= 10
    temp = number
    while number >= 10:
        number /= 10
    return temp, number

def top3(number):
    number -= int(number)
    return int(10 ** number)

def top4(number):
    number -= int(number)
    frequency[int(10 ** number) - 1] += 1

if __name__ == '__main__':
    N = 100000
    x = range(1, N+1)
    frequency = p.zeros(9, dtype=np.int)
    f = 1
    print '计算开始...'
    t0 = time()
    y = np.cumsum(np.log10(x))
    map(top4, y)
    t1 = time()
    print '耗时: ', t1 - t0
    print frenquency