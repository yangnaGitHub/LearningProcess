# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 14:23:50 2017

@author: natasha1_Yang
"""

import numpy as np
import matplotlib.pyplot as plt

def GetValue(block):
    temp = block**3#np.power
    tempmid = np.sin(block)**2
    temp = temp*tempmid
    tempmid = block**4 + 2*block**2 + 1
    temp = temp/tempmid
    return temp

if __name__ == "__main__":
    block = np.linspace(-5, 5, 100, endpoint=True, dtype=float)
    blockvalue = GetValue(block)
    print np.trapz(blockvalue, axis=0)
    plt.plot(block, blockvalue, 'r-', linewidth=2)
    plt.show()