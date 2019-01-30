# -*- coding: utf-8 -*-
"""
Created on Thu Jan 10 11:51:36 2019

@author: natasha_yang

@e-mail: ityangna0402@163.com
"""

import matplotlib.pyplot as plt
import numpy as np

x_data = np.linspace(-3, 3, 50)
y_data = 2*x_data + 1

plt.figure(num=1, figsize=(8, 5))
plt.plot(x_data, y_data, linewidth=10, zorder=1)

#移动坐标轴
ax = plt.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.spines['bottom'].set_position(('data', 0))
ax.yaxis.set_ticks_position('left')
ax.spines['left'].set_position(('data', 0))

#标注出点(x0, y0)的位置信息
x_c,y_c = 1,3
plt.plot([x_c, x_c], [0, y_c], 'k--', linewidth=2.5)#一条垂直的线[x_c,0 - x_c,y_c ]
#s是散点的大小,c(color)是颜色,alpha透明度
plt.scatter([x_c, ], [y_c, ], s=50, color='b')#标出点(x_c,y_c)

#添加注释annotate
plt.annotate('$2x+1=%s$' % y_c, xy=(x_c, y_c), xycoords='data',#显示信息,坐标,基于数据的值来选位置,
             xytext=(+30, -30), textcoords='offset points', fontsize=16,#标注位置的描述和xy偏差值
             arrowprops=dict(arrowstyle='->', connectionstyle="arc3,rad=.2"))#图中箭头类型的一些设置

#添加注释text
plt.text(-3.7, 3, r'$This\ is\ the\ some\ text. \mu\ \sigma_i\ \alpha_t$', fontdict={'size': 16, 'color': 'r'})#显示的位置,显示的message,字体大小和颜色

for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontsize(12)#重新调节字体大小
    label.set_bbox(dict(facecolor='white', edgecolor='None', alpha=0.7, zorder=2))#设置目的内容的透明度相关参数,facecolor前景色,edgecolor设置边框,alpha设置透明度

plt.show()