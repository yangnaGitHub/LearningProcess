# -*- coding: utf-8 -*-
"""
Created on Wed Dec 07 11:24:54 2016

@author: natasha1_Yang
"""

import os
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
#from sklearn.pipeline import Pipeline
#from sklearn import tree
#from sklearn.tree import DecisionTreeClassifier

#如何计算互信息
#如何建立一棵树
#防止过拟合的预剪枝+后剪枝(评价准则:生成K棵树,验证集上LOSS最小的那那棵树)
#如何后剪枝(计算所有节点的alpha,最小的alpha的节点将被剪枝掉)

#bagging
#重采样m次n个样本,构建m颗决策树,然后使用投票机制(比较灵活,如何造函数)

#样本不均衡的处理方式

def iris_type(s):
    it = {'Iris-setosa':0, 'Iris-versicolor':1, 'Iris-virginica':2}
    return it[s]

def relative_entropy(x_train, y_train):
#   使用互信息来选择属性做决策树
#   计算H(D)
    x_train_num = x_train.shape[0]
    y_train_num = y_train.shape[0]
    y_train_singal = np.zeros(3)
    for index in range(3):
        singal = 0
        for jndex in range(y_train_num):
            singal = singal + (index == y_train[jndex])
        y_train_singal[index] = float(singal) / y_train_num
#    print y_train_singal
    HD = 0
    for index in range(3):
        HD = HD - y_train_singal[index] * math.log(y_train_singal[index])
    print HD
    
#   计算H(D/A)
    Di = np.zeros((4, 5), dtype = np.float)
    for mnum in range(4):
        minval = min([x[mnum] for x in x_train])
        maxval = max([x[mnum] for x in x_train])
        Di[mnum] = np.linspace(minval, maxval + 0.1, 5, endpoint=True)
        print minval, maxval, maxval - minval
    
    Di_P = np.zeros((4, 4), dtype = np.float)
    Dik_P = np.zeros((4, 4, 3), dtype = np.float)
    for x_j in range(4):
        for x_i in range(x_train_num):
            for Di_j in range(4):
                if x_train[x_i][x_j] < Di[x_j][Di_j + 1]:
                    Di_P[x_j][Di_j] = Di_P[x_j][Di_j] + 1
                    Dik_P[x_j][Di_j][int(y_train[x_i])] = Dik_P[x_j][Di_j][int(y_train[x_i])] + 1
                    break

    for x_i in range(4):
        for x_j in range(4):
            Di_P[x_i][x_j] = float(Di_P[x_i][x_j]) / x_train_num
    print Di_P
    
    tempsum = 0;
    for x_i in range(4):
        for x_j in range(4):
            tempsum = sum(Dik_P[x_i][x_j])
            print tempsum
            for x_k in range(3):
                Dik_P[x_i][x_j][x_k] = Dik_P[x_i][x_j][x_k] / tempsum
    
    Calc_entropy = np.zeros((4, ), dtype = np.float)
    for x_i in range(4):#4个属性
        for x_j in range(4):#属性都分4个区间(4个value)
            for x_k in range(3):
                if Dik_P[x_i][x_j][x_k] == 0:
                    continue
                Calc_entropy[x_i] = Calc_entropy[x_i] - Di_P[x_i][x_j] * Dik_P[x_i][x_j][x_k] * math.log(Dik_P[x_i][x_j][x_k])
    return Calc_entropy
    
def DecisionTree(x_train, y_train, Depth = 3):
    relative_entropy(x_train, y_train)
    

iris_feature = u'花萼长度', u'花萼宽度', u'花瓣长度', u'花瓣宽度'

if __name__ == "__main__":
    os.chdir("E:\\MyOwner\\MyDocument\\ML_ChinaHadhoop\\10.RandomForest")
    mpl.rcParams['font.sans-serif'] = [u'SimHei']
    mpl.rcParams['axes.unicode_minus'] = False

    PATH = '..\\8.Regression\\8.iris.data'
    data = np.loadtxt(PATH, dtype=float, delimiter=',', converters={4: iris_type})
    x, y = np.split(data, (4,), axis=1)    
#    x = x[:, :2]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3, random_state=1)
    
    for index in range(5, 10, 5):
        DecisionTree(x_train, y_train, Depth = index)
