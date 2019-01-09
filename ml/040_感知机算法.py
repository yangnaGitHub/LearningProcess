# -*- coding: utf-8 -*-
"""
Created on Mon Feb 06 10:55:57 2017

@author: natasha1_Yang
"""
import numpy as np

if __name__ == "__main__":
    pointslist = [[1, 1, -1],
             [3, 3, 1],
             [4, 3, 1]
             ]
    points = np.array(pointslist)
    pointcount = points.shape[1]
    weight = np.zeros(2)
    b = 0
    while(1):
        num = 0
        for point in points:
            ret = point[0] * weight[0] + point[1] * weight[1] + b
            ret = ret * point[2]
            if ret <= 0:
                weight[0] = weight[0] + point[2] * point[0]
                weight[1] = weight[1] + point[2] * point[1]
                b = b + point[2]
            else:
                num += 1
        
        if num == pointcount:
            print("f(x) = sign((%d,%d)*x + %d)" % (weight[0], weight[1], b))
            break