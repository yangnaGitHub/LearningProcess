# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 14:52:11 2018

@author: natasha_yang

@e-mail: ityangna0402@163.com
"""

#计算size: filter_size + (n-1)*step_size = W + 2*padding
# => n = (W + 2P - F)/S + 1
#扩展卷积
# 在卷积的时候引进另一个参数=>扩展率:定义了卷积核中值与值之间的间隔
# 扩展率为2的3*3卷积核将具有与5*5卷积核相同的视野
# 相同的计算成本下,具有更宽的视野,可以捕捉更长的依赖关系
# 适用于需要更加宽泛的视野并且不用多个或更大卷积核的情况 => 实时图像分割
# WaveNet => https://arxiv.org/abs/1609.03499
#可变形卷积
# 规则的卷积核往往会限制特征抽取的有效性,让卷积核具有任意的形状,可以呈现随意的形状
# 可以重点关注一些重要的区域,能更有效的抽取输入图像的特征
# 进行2次卷积,第一次卷积计算得到offset的卷积核,第二次是利用第一步得到的offset卷积核进行常规卷积得到最终的输出
#  offset得到的通道数输出是input的通道数的2倍(有x和y的offset)
# Deformable convolution Network => https://arxiv.org/abs/1703.06211
#深度可分离的卷积
# 将卷积核操作拆分成多个步骤 => 卷积核K=k1.dot(k2)就是说通过k1和k2的卷积动作和通过K的卷积动作得到的卷积结果一致
# 比如: 1  2  1 ==> 1
#       0  0  0     0  * [1, 2, 1]  <== Sobel卷积
#      -1 -2 -1    -1
# 参数只需要6个,而不是之前的9个
# Xception Net:保持通道之间分离,然后按照深度方向进行卷积 => https://arxiv.org/abs/1610.02357
#Squeeze-and-Excitation
# 我们默认所有的通道是同等重要的,是否可以赋予给每个通道一个权重呢
# SEnet => https://arxiv.org/abs/1709.01507
#转置卷积
# 正常的过程:W=5, P=0, F=3, S=2 => n = (5-3)/2+1=2
# 反过来得到谁做F=(x=3), S=(y=2)的操作可以得到这个W=5的feature => W`=11
# https://buptldy.github.io/2016/10/29/2016-10-29-deconv/
#卷积基本不压缩图片,维度尽量保持不变,Pooling的时候在压缩