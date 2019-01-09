# -*- coding: utf-8 -*-

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

def calc_sin_small(x):
    x2 = -x ** 2
    t = x
    f = 1
    mysum = 0
    for index in range(10):
        mysum += t / f
        t *= x2
        f *= ((2 * index + 2) * (2 * index + 3))
    return mysum

if __name__ == "__main__":
    t = np.linspace(-2 * np.pi, 2 * np.pi, 100, endpoint=False)
    y = np.empty_like(t)
    a = t / (2 * np.pi)
    k = np.floor(a)
    a = t - k * 2 * np.pi
    for i ,x in enumerate(t):
        y[i] = calc_sin_small(x)
    mpl.rcParams['font.sans-serif'] = [u'SimHei']
    mpl.rcParams['axes.unicode_minus'] = False
    plt.figure(facecolor='w')
    plt.plot(t, y, 'r-', t, y, 'go', linewidth=2)
    plt.title(u'Taylor展开式', fontsize=18)
    plt.xlabel('x', fontsize=15)
    plt.ylabel('sin(x)', fontsize=15)
    plt.xlim((-7, 7))
    plt.ylim((-1.1, 1.1))    