# -*- coding: utf-8 -*-
"""
Created on Thu Mar 09 18:16:23 2017

@author: natasha1_Yang
"""

#某事件发生的概率小,则该事件的信息量大
#均匀分布的熵最大0≤H(X)≤lnN
#Var(X)= E(X2) - E2(x)
#E(X2) = E2(X) + Var(X) = μ2 +σ2
#H(X|Y) = H(X,Y)– H(Y)在Y发生的前提下,X发生“新”带来的熵
#条件熵的含义:x给定的情况下y的熵,相对于x求期望
#相对熵:(相对熵可以度量两个随机变量的“距离”)除非p和q相等,否则D(p||q)≠D(q||p)
#KL散度就是相对熵
#熵 - 互信息 = 条件熵==>I(X,Y) = H(Y) - H(Y|X) = H(X,Y) - H(X)
# _________________________
#|        |      |         |
#|H(X|Y)  |I(X,Y)|  H(Y|X) | ==> H(X, Y)
#|        |      |         |
#|________|______|_________|
#      H(X)        H(Y)