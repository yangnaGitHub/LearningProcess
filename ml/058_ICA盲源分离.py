# -*- coding: utf-8 -*-
"""
Created on Thu Mar 09 15:23:36 2017

@author: natasha1_Yang
"""

#ICA的著名应用是盲源分离
#假设n个人面前有n个话筒,然后这n个人说话时这n个话筒进行录音,这n个人说了m句话,最后从这n个话筒中收集一些录音,目标：从这些录音中分离出每个人的声音。
#S:源信号
#A:线性加权
#X:观测信号
#==> x = A.s ==> s = A逆.x ==> s = W.x
#目标:x已知,s目标,求W
#假设:源信号彼此间独立 + 源信号是非高斯分布(一组有确定方差的独立随机变量的和趋近于高斯分布)
#找到了一组“最不像高斯分布”的信号,则它们极有可能是源信号
#第i个源信号的概率密度函数为pi(s),第j时刻的n个源信号记做向量sj
import math  
import numpy as np  
import matplotlib.pyplot as plt  
   
def show_data(x,y):  
    num_list_x = np.arange(len(x))  
    plt.figure(figsize=(20, 10))  
    plt.xlim(0, len(num_list_x)+50)  
    plt.plot(num_list_x, x, color='b',linestyle='-', label='x')  
    plt.legend()  
    plt.show()  
    if y != None:  
        plt.figure(figsize=(20, 10))  
        num_list_y = np.arange(len(y))  
        plt.xlim(0, len(num_list_y)+50)  
        plt.plot(num_list_y, y, color='r',linestyle='-', label='y')  
        plt.legend()  
        plt.show()  
   
def logistic(t):  
    return 1.0/(1+np.exp(-t))  
   
def n_multiply(t, x):  
    return t * x  
   
def trans_inverse(x):  
    if not isinstance(x, np.ndarray):  
        x = np.array(x)  
    return np.linalg.inv(x.transpose())  
   
def ica(x):  
    m = len(x)      # 样本数目，这里是 2 个  
    n = len(x[0])   # mic 数目，这里是 1000 个  
    # 建立个 1000*1000 的列表  
    w = [[0.0]*n for t in range(n)]  
    # 建立个 1000*1000 的列表  
    iw = [[0.0]*n for t in range(n)]  
    # 建立个 1000*1000 的列表  
    w1 = [[0.0]*n for t in range(n)]  
    # 将对角线初始化为1  
    for i in range(n):  
        w[i][i] = 1  
    # 初始化学习率为  
    alpha = 0.001  
    # shuffle(x)  
    # 迭代次数最多不超过 200 次  
    for time in range(200):  
        # 分离出"样本数目"个样本  
        for i in range(m):  
            for j in range(n):  
                t = np.dot(w[j], x[i])  
                t = 1 - 2*logistic(t)  
                w1[j] = n_multiply(t,x[i])  # w1[j] = t*x[i]  
            iw = trans_inverse(w)    # iw = w^T^(-1)  
            iw = w1 + iw  
            w1 = np.add(w1, iw) #w1 += iw  
            w1 = np.dot(w1, alpha)  
            w = np.add(w, w1)  
        #print time, ":\t", w  
    return w  
   
def mix(A, x,y):  
    mix = np.dot(A, np.array([x, y]))#混合S和A
    #为何要把第一行的数据变成两行之和
    for i in xrange(len(mix[0])):
        mix[0][i] = mix[0][i] + mix[1][i]
   
    #show_data(mix[0], None)  
   
    return mix
   
def decode(w,x):
    ps = np.dot(x, w)
    return ps[0], ps[1]
   
   
if __name__ =="__main__":  
    s1 =[math.sin(float(x)/20) for x in range(0, 1000, 1)]  
    s2 = [float(x)/50 for x in range(0, 50, 1)]* 20  
    #s1 = [math.sin(float(x)/20) for x inrange(0, 100, 1)]  
    #s2 = [float(x)/50 for x in range(0, 50,1)] * 2  
    #show_data(s1, s2)  
   
    # 假定有N个人在说话，则在任何一个时刻，原始的源信号是N维的，混合信号也是N维的。从而，混合矩阵A和解混矩阵W都是N*N维的。——这个维度，和观测时间M无关。  
    # 即：混合矩阵A必须是N*N维，才能使得n维的原始信号乘上A后可以得到个n维的混合信号，解混矩阵同理。  
    A = [[0.6, 0.4], [0.45, 0.55]]  # 混合矩阵  
    x = mix(A, s1, s2)  #s1/s2线性加权得到输入数据x  
    # 去均值，这个老师的效果不错，但我这里反而变差了....  
    # 实际运用中还是要根据实际场合看看是否选取  
    x_mean = np.mean(x)  
    #plt.scatter(x[0], x[0], marker=".", c="g")
    #plt.scatter(x[1], x[1], marker="v", c="r")
    for i in xrange(x.shape[0]):  
        for j in xrange(x.shape[1]):  
            x[i][j] = x[i][j] - x_mean  
    # ica  
    w = ica(x)  
    # 解混  
    [ps1, ps2] = decode(w, x)  
    show_data(ps1, ps2)  