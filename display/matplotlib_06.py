# -*- coding: utf-8 -*-
"""
Created on Thu Jan 10 15:32:55 2019

@author: natasha_yang

@e-mail: ityangna0402@163.com
"""

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()#定义一个图像窗口
ax = Axes3D(fig)#在窗口上添加3D坐标轴

x_data = np.arange(-4, 4, 0.25)
y_data = np.arange(-4, 4, 0.25)
x_mesh, y_mesh = np.meshgrid(x_data, y_data)
z_mesh = np.sin(np.sqrt(x_mesh**2 + y_mesh**2))
#rstride:row的跨度,cstride:column的跨度,rainbow填充颜色
ax.plot_surface(x_mesh, y_mesh, z_mesh, rstride=1, cstride=1, cmap=plt.get_cmap('rainbow'))
#添加xy平面的等高线,zdir选择了x,效果将会是对于 XZ 平面的投影
ax.contourf(x_mesh, y_mesh, z_mesh, zdir='z', offset=-2, cmap=plt.get_cmap('rainbow'))

plt.show()