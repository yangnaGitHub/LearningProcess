# -*- coding: utf-8 -*-
"""
Created on Thu Jan 10 11:51:38 2019

@author: natasha_yang

@e-mail: ityangna0402@163.com
"""

import matplotlib.pyplot as plt
import numpy as np

count = 12
x_data = np.arange(count)
y_data_1 = (1 - x_data/float(count)) * np.random.uniform(0.5, 1.0, count)
y_data_2 = (1 - x_data/float(count)) * np.random.uniform(0.5, 1.0, count)

#plt.bar(x_data, +y_data_1)
#plt.bar(x_data, -y_data_2)
plt.bar(x_data, +y_data_1, facecolor='green', edgecolor='black')#facecolor主体颜色,edgecolor边框颜色
plt.bar(x_data, -y_data_2, facecolor='yellow', edgecolor='red')

plt.xlim(-0.5, count)
plt.ylim(-1.25, 1.25)
plt.xticks(())
plt.yticks(())

for x_v, y_v1, y_v2 in zip(x_data, y_data_1, y_data_2):
    # ha: horizontal alignment
    # va: vertical alignment
    plt.text(x_v + 0.2, y_v1 + 0.05, '%.2f' % y_v1, ha='center', va='bottom')#横向居中对齐,纵向底部对齐
    plt.text(x_v + 0.2, -y_v2 - 0.05, '%.2f' % y_v2, ha='center', va='top')#横向居中对齐,纵向顶部对齐

plt.show()