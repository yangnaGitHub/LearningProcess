# -*- coding: utf-8 -*-
"""
Created on Thu Jan 10 15:32:56 2019

@author: natasha_yang

@e-mail: ityangna0402@163.com
"""

import matplotlib.pyplot as plt
import numpy as np

def height_val(x_, y_):
    return (1 - x_/2 + x_**5 + y_**3) * np.exp(-x_**2 - y_**2)

count = 256
x_data = np.linspace(-3, 3, count)
y_data = np.linspace(-3, 3, count)
x_mesh, y_mesh = np.meshgrid(x_data, y_data)#256*256,meshgrid在二维平面中将每一个x和每一个y分别对应起来编织成栅格

#plt.contourf颜色填充,alpha透明度,8代表等高线的密集程度
plt.contourf(x_mesh, y_mesh, height_val(x_mesh, y_mesh), 8, alpha=.75, cmap=plt.cm.hot)
#进行等高线绘制,黑色线条宽度选0.5
C = plt.contour(x_mesh, y_mesh, height_val(x_mesh, y_mesh), 8, colors='black', linewidth=.5)
#添加高度数字,inline控制是否将Label画在线里面,字体大小为10,坐标轴隐藏
plt.clabel(C, inline=True, fontsize=10)
plt.xticks(())
plt.yticks(())
plt.show()