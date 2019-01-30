# -*- coding: utf-8 -*-
"""
Created on Wed Jan  9 19:26:44 2019

@author: natasha_yang

@e-mail: ityangna0402@163.com
"""

import matplotlib.pyplot as plt
import numpy as np

x_data = np.linspace(-3, 3, 50)
y_data_1 = 2*x_data + 1
y_data_2 = x_data**2
plt.figure()
plt.plot(x_data, y_data_2)
plt.plot(x_data, y_data_1, color='red', linewidth=1.0, linestyle='--')#曲线的颜色,曲线的宽度,曲线的类型
#plt.xlim设置x坐标轴范围
#plt.ylim设置y坐标轴范围
#plt.xlabel设置x坐标轴名称
#plt.ylabel设置y坐标轴名称
plt.xlim((-1, 2))
plt.ylim((-2, 3))
plt.xlabel('I am x')
plt.ylabel('I am y')
#plt.xticks设置x轴刻度以及名称
#plt.yticks设置y轴刻度以及名称
new_ticks = np.linspace(-1, 2, 5)
plt.xticks(new_ticks)
plt.yticks([-2, -1.8, -1, 1.22, 3],[r'$really\ bad$', r'$bad$', r'$normal$', r'$good$', r'$really\ good$'])
#plt.xticks(())#隐藏x轴
#plt.yticks(())#隐藏y轴
#plt.gca获取当前坐标轴信息
ax = plt.gca()
ax.spines['right'].set_color('none')#spines设置边框,set_color设置边框颜色
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')#xaxis.set_ticks_position设置x坐标刻度数字或名称的位置
ax.spines['bottom'].set_position(('data', 0))#spines设置边框,set_position设置边框位置
ax.yaxis.set_ticks_position('left')
ax.spines['left'].set_position(('data',0))
#plt.legend图例
plt.legend(loc='best')
plt.show()