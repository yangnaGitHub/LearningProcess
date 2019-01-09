# -*- coding: utf-8 -*-
"""
Created on Mon Feb 06 11:09:17 2017

@author: natasha1_Yang
"""

import numpy as np

if __name__ == "__main__":
    pointslist = [[3, 3, 1],
             [4, 3, 1],
             [1, 1, -1]
             ]
    points = np.array(pointslist)
    pointcount = points.shape[1]
    GramMatrix = np.zeros((pointcount, pointcount))#3 * 3内积矩阵
    for xindex in range(pointcount):
        for yindex in range(pointcount):
            GramMatrix[xindex][yindex] = points[xindex][0] * points[yindex][0] + points[xindex][1] * points[yindex][1]
    
    weight = np.zeros(2)
    ai = np.zeros(pointcount)
    b = 0
    while(1):
        num = 0
        for yindex in range(pointcount):
            ret = 0;
            for xindex in range(pointcount):
                ret += ai[xindex] * points[xindex][2] * GramMatrix[xindex][yindex]
            ret += b
            ret = ret * points[yindex][2]
            if ret <= 0:
                ai[yindex] += 1
                b = b + points[yindex][2]
            else:
                num += 1
        
        if num == pointcount:
            for xindex in range(pointcount):
                weight[0] += ai[xindex] * points[xindex][0] * points[xindex][2]
                weight[1] += ai[xindex] * points[xindex][1] * points[xindex][2]
            print("f(x) = sign((%d,%d)*x + %d)" % (weight[0], weight[1], b))
            break