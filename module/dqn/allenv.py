# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 10:26:27 2019

@author: yangna

@e-mail: ityangna0402@163.com
"""

import numpy as np
import time
import sys
if sys.version_info.major == 2:
    import Tkinter as tk
else:
    import tkinter as tk
from conf.conf import args

class Maze(tk.Tk, object):
    MAZE_H = args.get_option('MAZE', 'MAZE_H', 'int')
    UNIT = args.get_option('MAZE', 'UNIT', 'int')
    MAZE_W = args.get_option('MAZE', 'MAZE_W', 'int')
    
    def __init__(self):
        super(Maze, self).__init__()
        self.action_space = ['u', 'd', 'l', 'r']
        self.n_actions = len(self.action_space)
        self.n_features = 4
        self.title('maze')
        self.geometry('{0}x{1}'.format(self.MAZE_H * self.UNIT, self.MAZE_H * self.UNIT))#160*160
        self._build_maze()

    def _build_maze(self):
        self.canvas = tk.Canvas(self, bg='white', height=self.MAZE_H * self.UNIT, width=self.MAZE_W * self.UNIT)
        
        #创建网格
        for col in range(0, self.MAZE_W * self.UNIT, self.UNIT):
            self.canvas.create_line(col, 0, col, self.MAZE_H * self.UNIT)
        for row in range(0, self.MAZE_H * self.UNIT, self.UNIT):
            self.canvas.create_line(0, row, self.MAZE_W * self.UNIT, row)

        
        origin = np.array([20, 20])#远点

        #第1行2列的黑方块
        hell1_center = origin + np.array([self.UNIT * 2, self.UNIT])#100, 60
        self.hell1 = self.canvas.create_rectangle(
                hell1_center[0] - 15, hell1_center[1] - 15,#85,45
                hell1_center[0] + 15, hell1_center[1] + 15,#115,75 
                fill='black')
        #第2行1列的黑方块
        hell2_center = origin + np.array([self.UNIT, self.UNIT * 2])#60, 100
        self.hell2 = self.canvas.create_rectangle(
                hell2_center[0] - 15, hell2_center[1] - 15,
                hell2_center[0] + 15, hell2_center[1] + 15, fill='black')

        #黄圆的地方
        oval_center = origin + self.UNIT * 2
        self.oval = self.canvas.create_oval(
                oval_center[0] - 15, oval_center[1] - 15,
                oval_center[0] + 15, oval_center[1] + 15, fill='yellow')

        #红方块的地方
        self.rect = self.canvas.create_rectangle(
                origin[0] - 15, origin[1] - 15,
                origin[0] + 15, origin[1] + 15,
                fill='red')

        #展开
        self.canvas.pack()

    def reset(self):
        self.update()
        time.sleep(0.5)
        #重新画还原
        self.canvas.delete(self.rect)
        origin = np.array([20, 20])
        self.rect = self.canvas.create_rectangle(
                origin[0] - 15, origin[1] - 15,
                origin[0] + 15, origin[1] + 15,
                fill='red')
        return self.canvas.coords(self.rect)#返回他的坐标

    def step(self, action):
        state = self.canvas.coords(self.rect)#获得坐标
        base_action = np.array([0, 0])
        if action == 0:#上
            if state[1] > self.UNIT:
                base_action[1] -= self.UNIT
        elif action == 1:#下
            if state[1] < (self.MAZE_H - 1) * self.UNIT:
                base_action[1] += self.UNIT
        elif action == 2:#右
            if state[0] < (self.MAZE_W - 1) * self.UNIT:
                base_action[0] += self.UNIT
        elif action == 3:#左
            if state[0] > self.UNIT:
                base_action[0] -= self.UNIT

        self.canvas.move(self.rect, base_action[0], base_action[1])#移动到目标地方

        state_ = self.canvas.coords(self.rect)#获得移动后的坐标

        # reward function
        if state_ == self.canvas.coords(self.oval):#如果移动到黄色的圆点处就完成
            reward = 1
            done = True
            #state_ = 'terminal'
        elif state_ in [self.canvas.coords(self.hell1), self.canvas.coords(self.hell2)]:#移动到障碍处就惩罚他
            reward = -1
            done = True
            #state_ = 'terminal'
        else:
            reward = 0
            done = False

        return state_, reward, done

    def render(self):
        time.sleep(0.1)
        self.update()
#def update():
#    for _ in range(10):
#        state = env.reset()
#        while True:
#            env.render()
#            action = 1
#            state, reward, done = env.step(action)
#            if done:
#                break

#if __name__ == '__main__':
#    env = Maze()
#    env.after(100, update)
#    env.mainloop() 