# -*- coding: utf-8 -*-
"""
Created on Thu Jan 10 16:51:09 2019

@author: natasha_yang

@e-mail: ityangna0402@163.com
"""

import matplotlib.pyplot as plt

plt.figure()
plt.subplot(2, 2, 1)#2*2个中的第一个
plt.plot([0, 1], [0, 1])

plt.subplot(2, 2, 2)
plt.plot([0, 1], [0, 2])

plt.subplot(223)
plt.plot([0, 1], [0, 3])

plt.subplot(224)
plt.plot([0, 1], [0, 4])
plt.show()

#不均匀图中图
plt.figure()
plt.subplot(2, 1, 1)#第一行
plt.plot([0, 1], [0, 1])

plt.subplot(2, 3, 4)#第二行,第一行3个,所以第二行开始的是编号4
plt.plot([0, 1], [0, 2])

plt.subplot(235)
plt.plot([0, 1], [0, 3])

plt.subplot(236)
plt.plot([0, 1], [0, 4])
plt.show()

#分格显示
####subplot2grid
plt.figure()
#(3,3)表示将整个图像窗口分成3行3列,(0,0)表示从第0行第0列开始作图,colspan=3表示列的跨度为3,rowspan=1表示行的跨度为1
#---
ax1 = plt.subplot2grid((3, 3), (0, 0), colspan=3)
ax1.plot([1, 2], [1, 2])
ax1.set_title('ax1_title')

#从第1行第0列开始作图
#---
#  -
ax2 = plt.subplot2grid((3, 3), (1, 0), colspan=2)
ax3 = plt.subplot2grid((3, 3), (1, 2), rowspan=2)
#--
ax4 = plt.subplot2grid((3, 3), (2, 0))
ax5 = plt.subplot2grid((3, 3), (2, 1))
#ax4.scatter创建一个散点图,使用ax4.set_xlabel和ax4.set_ylabel来对x轴和y轴命名
ax4.scatter([1, 2], [2, 2])
ax4.set_xlabel('ax4_x')
ax4.set_ylabel('ax4_y')
plt.show()

####gridspec
import matplotlib.gridspec as gridspec
#gridspec.GridSpec将整个图像窗口分成3行3列
plt.figure()
gs = gridspec.GridSpec(3, 3)
#---
ax6 = plt.subplot(gs[0, :])
#---
#  -
ax7 = plt.subplot(gs[1, :2])
ax8 = plt.subplot(gs[1:, 2])
#--
ax9 = plt.subplot(gs[-1, 0])
ax10 = plt.subplot(gs[-1, -2])
plt.show()

####subplots
#2行2列的图像窗口,sharex=True共享x轴坐标,sharey=True共享y轴坐标
f, ((ax11, ax12), (ax13, ax14)) = plt.subplots(2, 2, sharex=True, sharey=True)
#ax11.scatter创建一个散点图
ax11.scatter([1, 2], [1, 2])
#紧凑显示图像
plt.tight_layout()
plt.show()