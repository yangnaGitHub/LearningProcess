# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 18:17:20 2019

@author: natasha_yang

@e-mail: ityangna0402@163.com
"""

L1正则=>alpha*(权值w的绝对值之和)
 带有绝对值符号的函数,是不完全可微的
 L1正则函数有很多突出的角,损失函数和这些角接触的几率会远远大于于其他部位接触的几率
 而这些角会有很多权值等于0=>L1可以产生稀疏模型,进而可以用于特征选择
 而alpha可以控制参数值的大小,当系数很小的时候,得到的最优解会很小,可以达到L2正则类似的效果
 适用于特征之间有关联的情况
L2正则=>使得每个w元素都小,都接近于0,而越小的参数说明模型越简单,越简单的模型越不容易产生过拟合
 适用于特征之间没有关联的情况
L1和L2的优点可以结合起来就是Elastic Net
当多个特征和另一个特征相关的时候弹性网络非常有用
https://www4.stat.ncsu.edu/~post/josh/LASSO_Ridge_Elastic_Net_-_Examples.html
