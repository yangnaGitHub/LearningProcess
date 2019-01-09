# -*- coding: utf-8 -*-
"""
Created on Tue Feb 07 15:20:26 2017

@author: natasha1_Yang
"""

import numpy as np

def GetProY(points):
    index = 0
    positive = 0
    negative = 0
    for point in points:
        if '1' == point[2]:
            positive += 1
        if '-1' == point[2]:
            negative += 1
        index += 1
    #print index, positive, negative
    proy = np.zeros(2)
    proy[0] = float(positive)/float(index)
    proy[1] = float(negative)/float(index)
    #print proy
    return proy
    
def GetProYGiveX(points):
    Data = [[0 for xindex in range(2)] for yindex in range(12)]#np.zeros((2 * 3 + 2 * 3, 2))
    countp = [point[2] for point in points].count('1')
    countn = [point[2] for point in points].count('-1')
    #print countp, countn
    tag = 0
    for xindex in range(2):
        ExistList = set(point[xindex] for point in points)
        #print ExistList
        for index in ExistList:
            count = [point[xindex] for point in points if '1' == point[2]].count(index)
            #print "1", index, count
            Data[tag][0] = index
            Data[tag][1] = float(count)/float(countp)
            count = [point[xindex] for point in points if '-1' == point[2]].count(index)
            #print "-1", index, count
            Data[6 + tag][0] = index
            Data[6 + tag][1] = float(count)/float(countn)
            tag += 1
    return Data
    
def GetResult(proy, proygivex, Target):
    pthpro = [Spro[1] for Spro in proygivex if Spro[0] in Target]
    pro = [0, 0]
    for xindex in range(2):
        pro[xindex] = proy[xindex] * pthpro[2 * xindex] * pthpro[(2 * xindex) + 1]

if __name__ == "__main__":
    pointslist = [[1, 'S', -1],[1, 'M', -1],
                  [1, 'M', 1],[1, 'S', 1],
                  [1, 'S', -1],[2, 'S', -1],
                  [2, 'M', -1],[2, 'M', 1],
                  [2, 'L', 1],[2, 'L', 1],
                  [3, 'L', 1],[3, 'M', 1],
                  [3, 'M', 1],[3, 'L', 1],
                  [3, 'L', -1]
                  ]
    points = np.array(pointslist)
    proy = GetProY(points)
    proygivex = GetProYGiveX(points)
    Target = ['2', 'S']
    GetResult(proy, proygivex, Target)