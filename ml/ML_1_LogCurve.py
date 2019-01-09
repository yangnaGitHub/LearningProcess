# -*- coding: utf-8 -*-
"""
Created on Tue Nov 08 08:49:46 2016

@author: natasha1_Yang
"""

import math
import matplotlib.pyplot as plt

if __name__ == "__main__":
    x = [float(i) / 100.0 for i in range(1, 300)]
    y = [math.log(i) for i in x]
    plt.plot(x, y, 'r-', linewidth=3, label='log curve')
    a = [x[20], x[175]]
    b = [y[20], y[175]]
    plt.plot(a, b, 'g-', linewidth=2)
    plt.plot(a, b, 'b*', markersize=15, alpha=0.75)
    plt.legend(loc='upper left')
    plt.grid(True)
    plt.xlabel('x')
    plt.ylabel('log(x)')
    plt.show()