# -*- coding: utf-8 -*-
"""
Created on Tue Feb 07 17:35:02 2017

@author: natasha1_Yang
"""

import numpy as np
import math

def GetEntropy(data):
    All = [index[4] for index in data]
    Count1 = (float)(All.count(1)) / (float)(len(All))
    Count0 = (float)(All.count(0)) / (float)(len(All))
    return -Count1 * math.log(Count1) - Count0 * math.log(Count0)

def GetCrossEntropy(data, FeatureList):
    All = [index[4] for index in data]
    FeatureEntropy = np.zeros(len(FeatureList));
    for index in range(len(FeatureList)):
        if 0 == FeatureList[index]:
            temps = [gettemp[index] for gettemp in data]
            setlist = list(set(temps))
            count = np.zeros(len(setlist))
            FeatureEntropy[index] = 0
            for temp in range(len(setlist)):
                count[temp] = float(temps.count(setlist[temp])) / float(len(temps))
                pos = 0;
                neg = 0;
                for mindex in range(len(temps)):
                    if setlist[temp] == temps[mindex]:
                        if 1 == All[mindex]:
                            pos += 1
                        if 0 == All[mindex]:
                            neg += 1
                if pos != 0:
                    pos = float(pos) / float(pos + neg)
                else:
                    pos = 0
                neg = 1 - pos
                FeatureEntropyTemp = 0
                if pos != 0:
                    FeatureEntropyTemp += -pos * math.log(pos)
                if neg != 0:
                    FeatureEntropyTemp += -neg * math.log(neg)
                FeatureEntropy[index] += (count[temp] * FeatureEntropyTemp)
    return FeatureEntropy

def DecisionTree(data, FeatureList, ClassfierIndex):
    All = [index[4] for index in data]
    ListAll = list(set(All))
    if 1 == len(ListAll):
        print "Feature:", ClassfierIndex
        print data
        return
    H_T = GetEntropy(data)
    FeatureEntropy = GetCrossEntropy(data, FeatureList)
    FeatureEntropy = H_T - FeatureEntropy
    for index in range(len(FeatureEntropy)):
        if FeatureEntropy[index] == max(FeatureEntropy):
            FeatureList[index] = 1
            temps = [temp[index] for temp in data]
            listtemp = list(set(temps))
            for mindex in range(len(listtemp)):
                tempdata = np.zeros((temps.count(listtemp[mindex]), 5), dtype = int)
                kindex = 0
                for nindex in range(len(temps)):
                    if temps[nindex] == listtemp[mindex]:
                        tempdata[kindex] = data[nindex]
                        kindex += 1
                DecisionTree(tempdata, FeatureList, index)
            break
    
if __name__ == "__main__":
    data = np.loadtxt("045_DTDATA.csv", dtype=int, delimiter=',', usecols=(range(1, 6)))#useclos使用那些列,skiprows跳过那些列
    FeatureList = [0, 0, 0, 0]
    DecisionTree(data, FeatureList, 0)
    #决策树ID3算法
#  [[ 0.,  0.,  0.,  0.,  0.],
#   [ 0.,  0.,  0.,  1.,  0.],
#   [ 0.,  1.,  0.,  1.,  1.],
#   [ 0.,  1.,  1.,  0.,  1.],
#   [ 0.,  0.,  0.,  0.,  0.],
#   [ 1.,  0.,  0.,  0.,  0.],
#   [ 1.,  0.,  0.,  1.,  0.],
#   [ 1.,  1.,  1.,  1.,  1.],
#   [ 1.,  0.,  1.,  2.,  1.],
#   [ 1.,  0.,  1.,  2.,  1.],
#   [ 2.,  0.,  1.,  2.,  1.],
#   [ 2.,  0.,  1.,  1.,  1.],
#   [ 2.,  1.,  0.,  1.,  1.],
#   [ 2.,  1.,  0.,  2.,  1.],
#   [ 2.,  0.,  0.,  0.,  0.]]
#    data[0]:0青年 1中年 2老年
#    data[1]:0没有工作 1有工作
#    data[2]:0没有自己的房子 1有自己的房子
#    data[3]:0信贷情况一般 1信贷情况好 2信贷情况非常好
#    data[4]:0不能贷到款 1能贷到款
#   熵:根据分类结果data[4]来计算(1的个数为9 0的个数为6)H(T)= -(9/15)*log(9/15) - (6/15)*log(6/15)
#   条件熵:A代表年龄(青年中年中年各5个人)H(T|A) = (5/15)H(青年) + (5/15)H(中年) + (5/15)H(老年)
#       H(青年) = 可以贷款的青年2 + 不可以贷款的青年3 = -(2/5)log(2/5) - (3/5)log(3/5)
#       同理中年和老年,同理是否有工作,是否房子和信贷情况
#   计算信息增益:h(T,A) = H(T) - H(T|A),同理计算其他的增益 PS:C4.5就是将信息增益换成信息增益比
#   max(信息增益)作为根节点,分为数据集T1 & T2
#   由于T1中所有的数据都属于一类,所以作为一个叶子节点
#   针对T2中的数据集在剩余的特征中调用前面的步骤
    