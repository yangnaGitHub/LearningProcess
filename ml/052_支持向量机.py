# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 17:52:05 2017

@author: natasha1_Yang
"""
#核方法:找出并学习一组数据中的相互关系,用来解决非线性模式分析问题
#思想:通过某种非线性映射将原始数据嵌入到合适的高维特征空间,在通用的线性学习器在这个新的空间中分析和处理模式
#基于假设:在低维空间中不能线性分割的点集,通过转化为高维空间中的点集时,很可能变为线性可分的
#任何半正定的函数都可以作为核函数
#导致维度祸根,每一个点都必须先转换到高维度空间然后求取分割平面的参数
#Kernel trick:核函数K(x1,x2)= <φ(x1),φ(x2)>(x1和x2是低维度空间中点,φ(xi)是低维度空间的点xi转化为高维度空间中的点的表示,<,> 表示向量的内积)
#参数学习的形式(学习参数)和基于实例的学习形式(在预测的时候使用训练数据)
#二次规划:
#设M是n阶方阵,如果对任何非零向量z,都有z转置*M*z>0就称M正定矩阵,如果z转置*M*z≥0就称M是半正定矩阵
#不适定问题:
#正则化(避免出现过拟合):对最小化经验误差函数上加约束,这样的约束可以解释为先验知识(正则化参数等价于对参数引入先验分布)
#欧式空间:
#线性空间(主要研究集合的描述:基)+度量空间
#赋范线性空间 = 线性空间 + 范数(长度)
#内积空间 = 赋范线性空间 + 内积(角度)
#完备的内积空间就称为Hilbert空间
#支持向量:训练数据集的样本点中与分离超平面距离最近的样本点的实例称为支持向量
#决定分离超平面时只有支持向量起作用,支持向量机由很少的“重要的”训练样本确定
#正则化的合页损失函数的最小化问题
#函数间隔 + 几何间隔(函数间隔确定)
#支持向量机就是找出几何间隔最大(硬间隔最大化)的分离超平面
#eg:x1(3, 3) x2(4, 3) x3(1, 1),其中y1=1 y2=1 y3=-1,求最大间隔分离超平面
#根据最大间隔法,构造约束最优化问题:
#    min(w, b) 1/2(w1^2 + w2^2)
#    s.t. 3w1+3w2+b >= 1
#         4w1+3w2+b >= 1
#         -w1-w2-b >= 1
#    ==>w1 = w2 = 1/2, b = -2
#使损失函数尽量小,间隔尽量大,使误分类点的个数尽量最小,添加C作为惩罚参数==>软间隔最大化
#合页损失函数(hinge loss)
#SMO:序列最小化算法,用于解决凸二次规划对偶问题十分低效