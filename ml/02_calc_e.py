# -*- coding: utf-8 -*-

import numpy as np
import math
import matplotlib as mpl
import matplotlib.pyplot as plt

def calc_e_small(x):
    n = 10
    f = np.arange(1, n + 1).cumprod()#累积连乘
    #[1, 2, 6, 24, 120, 720, 5040, 40320, 362880, 3628800]
    b = np.array([x] * n).cumprod()
    return np.sum(b / f) + 1

def calc_e(x):
    reverse = False
    if x < 0:
        x = -x
        reverse = True
    In2 = 0.69314718055994530941723212145818
    c = x / In2
    a = int(c + 0.5)
    b = x - a * In2
    y = (2**a) * calc_e_small(b)
    if reverse:
        return 1 / y
    return y

if __name__ == "__main__":
    t1 = np.linspace(-2, 0, 10, endpoint=False)
    t2 = np.linspace(0, 3, 20)
    t = np.concatenate((t1, t2))
    print t
    y = np.empty_like(t)
    for i, x in enumerate(t):
        y[i] = calc_e(x)
        print "e**", x, " = ", y[i], "\t", math.exp(x)
    plt.figure(facecolor="w")
    mpl.rcParams['font.sans-serif'] = [u'SimHei']
    mpl.rcParams['axes.unicode_minus'] = False
    plt.plot(t, y, 'r-', t, y, 'go', linewidth=2)
    plt.title(u'Taylor展开式', fontsize=18)
    plt.xlabel('x', fontsize=15)
    plt.ylabel('exp(x)', fontsize=15)
    plt.grid(True)
    plt.show()