# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 15:41:56 2016

@author: natasha1_Yang
"""

import numpy as np

def restore(sigma, u, v, K):#奇异值,左奇异向量,右奇异向量
    print K
    m = len(u)
    n = len(v[0])
    a = np.zeros((m, n))
    for k in range(K + 1):
        for index  in range(m):
            a[index] += sigma[k] * u[index][k] * v[k]
    b = a.astype('uint8')
    Image.formarray(b).save("svd_" + str(K) + ".png")