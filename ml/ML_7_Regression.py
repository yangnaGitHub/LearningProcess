# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import math
from pprint import pprint
import os
import numpy as np
import matplotlib.pyplot as plt

#####一种正则方式
#LSR是一种通过在输出中添加噪声(noise)对模型约束,降低模型过拟合程度的一种正则方法
#为了缓解由于label不够平衡问导致的过拟合问题
#q(y|x)是y的真实分布,u(y)是独立于样本的一直的关于y的分布 ==> q`(y|x) = (1 e) * q(y|x) + e * u(y)
# 构成一个新的分布,就是在y中加入噪声,其中一半u(y) = 1/K(分类的count)
# ==> q`(y|x) = (1-e)*q(y|x) + e/K

def MySplitDate(x_val, y_val, Split = 5):
    lenx = int(math.ceil(x_val.shape[0] / Split))
    leny = int(math.ceil(y_val.shape[0] / Split))
    x_test = x_val[:lenx]
    x_train = x_val[lenx:]
    y_test = y_val[:leny]
    y_train = y_val[leny:]
    return x_train, y_train, x_test, y_test
    
#y - h(x)
def Diff(x_val, y_val, theta):
    prenum = len(theta)
    presum = 0
    for i in range(prenum):
        presum += x_val[i] * theta[i]
    
    return y_val - presum 

#随机梯度下降
def LinearRegression(x_train, y_train, theta, alpha = 0.001):
    prenum = len(theta)
    for i in range(10000):
        differror = 0;
        for x, y in zip(x_train, y_train):#一个样本
            diff = Diff(x, y, theta)
            for gradindex in range(prenum):
                theta[gradindex] += alpha * diff * x[gradindex]#一个样本做一次
            differror += Diff(x, y, theta) ** 2
        differror /= 2;
        print theta, "differror = ", differror
        
    return theta

#批量梯度下降
def LinearRegressionAll(x_train, y_train, theta, alpha = 0.001):
    prenum = len(theta)
    for i in range(1000):
        differror = 0;
        AllGrad = np.zeros(prenum);
        for x, y in zip(x_train, y_train):#一个样本
            diff = Diff(x, y, theta)
            for gradindex in range(prenum):
                AllGrad[gradindex] += alpha * diff * x[gradindex]#每个样本特征叠加
        for gradindex in range(prenum):
                theta[gradindex] += AllGrad[gradindex]#批量
        for x, y in zip(x_train, y_train):
            differror += Diff(x, y, theta) ** 2
        differror /= 2;
        print theta, "differror = ", differror
        
    return theta
    
def Predict(x_test, theta):
    dim = x_test.shape[0]
    prenum = len(theta)
    presum = 0
    y_test = np.zeros(dim)
    for index in range(dim):
        for i in range(prenum):
            presum += x_test[index][i] * theta[i]
        y_test[index] = presum
    return y_test

if __name__ == "__main__":
    #GetData
    os.chdir("E:\\MyOwner\\MyDocument\\ML_ChinaHadhoop\\8.Regression")
    with open("8.Advertising.csv", "rb") as f:
        x_val = []
        y_val = []
        for row, context in enumerate(f):
            if row == 0:
                continue
            context = context.strip()
            if not context:
                continue
            context = map(float, context.split(","))
            x_val.append(context[1:-1])
            y_val.append(context[-1])
    
#    #bias + SplitData 
    x_val = np.array(x_val)
    y_val = np.array(y_val)    
    x_val = np.hstack([x_val, np.ones((x_val.shape[0], 1))])
    x_train, y_train, x_test, y_test = MySplitDate(x_val, y_val)
    
    #3 <== features, Model = 00 + 01x1 + 02x2 + 03x3
    #inittheta
    theta = np.random.normal(0, 1, 4)
    
    #Learning
    theta = LinearRegression(x_train, y_train, theta, alpha = 0.000005)
    theta = LinearRegressionAll(x_train, y_train, theta, alpha = 0.0000002)
    
    #test
    y_hat = Predict(x_test, theta)
    
    #compare result
    t = np.arange(len(x_test))
    plt.plot(t, y_test, 'r-', linewidth=2, label='Test')
    plt.plot(t, y_hat, 'g-', linewidth=2, label='Predict')
    plt.legend(loc='upper right')
    plt.grid()
    plt.show()