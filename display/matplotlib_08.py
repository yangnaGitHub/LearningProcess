# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 15:24:18 2019

@author: natasha_yang

@e-mail: ityangna0402@163.com
"""

#import matplotlib.pyplot as plt
from matplotlib import pyplot as plt

fig = plt.figure()

x_data = [1, 2, 3, 4, 5, 6, 7]
y_data = [1, 3, 4, 2, 5, 8, 6]

#绘制大图
#确定大图左下角的位置以及宽高,占整个figure坐标系的百分比
left, bottom, width, height = 0.1, 0.1, 0.8, 0.8
ax1 = fig.add_axes([left, bottom, width, height])
ax1.plot(x_data, y_data, 'r')
ax1.set_xlabel('x axis')
ax1.set_ylabel('y axis')
ax1.set_title('big picture')

#绘制小图
left, bottom, width, height = 0.2, 0.6, 0.25, 0.25
ax2 = fig.add_axes([left, bottom, width, height])
ax2.plot(y_data, x_data, 'b')
ax2.set_xlabel('left x')
ax2.set_ylabel('left y')
ax2.set_title('mini 1')

plt.axes([0.6, 0.2, 0.25, 0.25])
plt.plot(y_data[::-1], x_data, 'g') # 注意对y进行了逆序处理
plt.xlabel('right x')
plt.ylabel('right y')
plt.title('mini 2')
plt.show()

import numpy as np

x_data = np.arange(0, 10, 0.1)
y_data_1 = 0.05 * x_data**2
y_data_2 = -1 * y_data_1
#第一个y坐标
fig, ax1 = plt.subplots()
#第二个y坐标,调用twinx()方法
ax2 = ax1.twinx()
ax1.plot(x_data, y_data_1, 'g-')
ax1.set_xlabel('x axis')
ax1.set_ylabel('y1 axis', color='g')
ax2.plot(x_data, y_data_2, 'b-')
ax2.set_ylabel('y2 axis', color='b')

plt.show()

from matplotlib import animation

fig, ax = plt.subplots()
x_data = np.arange(0, 2*np.pi, 0.01)
line, = ax.plot(x_data, np.sin(x_data))

#构造自定义动画函数animate
def animate(index):
    line.set_ydata(np.sin(x_data + index/10.0))
    return line
#构造开始帧函数init
def init():
    line.set_ydata(np.sin(x_data))
    return line
#参数设置,调用FuncAnimation函数生成动画
ani = animation.FuncAnimation(fig=fig,#进行动画绘制的figure
                              func=animate,#自定义动画函数
                              frames=100,#动画长度,一次循环包含的帧数
                              init_func=init,#自定义开始帧
                              interval=20,#更新频率,以ms计
                              blit=False)#选择更新所有点,还是仅更新产生变化的点
plt.show()
#apt-get install ffmpeg
#ani.save('basic_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])#将动画以mp4格式保存下来