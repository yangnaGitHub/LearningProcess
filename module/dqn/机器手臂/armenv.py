# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 14:14:42 2019

@author: yangna

@e-mail: ityangna0402@163.com
"""

import numpy as np

class ArmEnv(object):#手臂的逻辑运动和动作等
    state_shape = 2#2个观测值
    action_shape = 2#2个动作
    #转动角度范围
    action_threshold =  [-1, 1]
    dis = None
    #目标点
    goal = {'x_val': 100., 'y_val': 100., 'l_val': 40}
    dt = 0.1
    
    def __init__(self):
        #[(100., 0.5235988), (100., 0.5235988)]
        self.arm_info = np.zeros(2, dtype=[('len', np.float32), ('ran', np.float32)])
        self.arm_info['len'] = 100#两段手臂的长度
        self.arm_info['ran'] = np.pi/6#两段手臂的旋转角度
        
    def reset(self):
        self.arm_info['ran'] = 2*np.pi*np.random.rand(2)
        return self.arm_info['ran']
    
    def sample_action(self):
        return np.random.rand(2)-0.5
    
    def render(self):
        if self.dis is None:
            self.dis = display(self.arm_info, self.goal)
        self.dis.render()
    
    def step(self, action):
        done = False
        reward = 0.
        #计算单位时间dt内旋转的角度,将角度限制在360度以内
        action = np.clip(action, *self.action_threshold)
        self.arm_info['ran'] += action * self.dt
        self.arm_info['ran'] %= np.pi * 2
        #将两截手臂的角度信息当做一个state
        state = self.arm_info['ran']
        #计算finger的坐标如果接触到goal,回合结束
        (a1l, a2l) = self.arm_info['len']
        (a1r, a2r) = self.arm_info['ran']
        a1xy = np.array([200., 200.])
        a1xy_ = np.array([np.cos(a1r), np.sin(a1r)]) * a1l + a1xy
        finger = np.array([np.cos(a1r + a2r), np.sin(a1r + a2r)]) * a2l + a1xy_

        #根据finger和goal的坐标得出done和reward
        if (self.goal['x_val'] - self.goal['l_val']/2 < finger[0] < self.goal['x_val'] + self.goal['l_val']/2) and (self.goal['y_val'] - self.goal['l_val']/2 < finger[1] < self.goal['y_val'] + self.goal['l_val']/2):
            done = True
            reward = 1.
        return state, reward, done
    
    def close(self):
        self.dis.stopandclose()

#API的路径https://pythonhosted.org/pyglet/
import pyglet#https://pyglet.readthedocs.io/en/pyglet-1.3-maintenance/#
class display(pyglet.window.Window):#手臂的可视化
    bar_thc = 5
    def __init__(self, arm_info, goal):#画机械手臂
        # vsync是True,按屏幕频率刷新,False就不按照那个频率
        super(display, self).__init__(width=400, height=400, resizable=False, caption='Arm', vsync=False)
        
        self.arm_info = arm_info
        self.center_coord = np.array([200, 200])#添加窗口中心点,手臂的起始点
        
        pyglet.gl.glClearColor(1, 1, 1, 1)#窗口背景的颜色
        self.batch = pyglet.graphics.Batch()#刷子
        #添加蓝点
        self.goal = self.batch.add(
                #pyglet.gl.GL_QUADS的说明https://pyglet.readthedocs.io/en/pyglet-1.3-maintenance/programming_guide/graphics.html
                4, pyglet.gl.GL_QUADS, None,#4个点
                #'v2f'和'c3B'的说明
                #https://pyglet.readthedocs.io/en/pyglet-1.3-maintenance/programming_guide/graphics.html#vertex-attributes
                ('v2f', [goal['x_val'] - goal['l_val'] / 2, goal['y_val'] - goal['l_val'] / 2,#x1,y1
                         goal['x_val'] - goal['l_val'] / 2, goal['y_val'] + goal['l_val'] / 2,#x2,y2
                         goal['x_val'] + goal['l_val'] / 2, goal['y_val'] + goal['l_val'] / 2,#x3,y3
                         goal['x_val'] + goal['l_val'] / 2, goal['y_val'] - goal['l_val'] / 2]),#x4,y4
                ('c3B', (86, 109, 249) * 4))#c3B表示的是这个物体的颜色,4个顶点都是(86, 109, 249)
        #添加一条手臂
        self.arm1 = self.batch.add(
                4, pyglet.gl.GL_QUADS, None,
                ('v2f', [250, 250,
                         250, 300,
                         260, 300,
                         260, 250]),
                ('c3B', (249, 86, 86) * 4,))
        #添加第二条手臂
        self.arm2 = self.batch.add(
                4, pyglet.gl.GL_QUADS, None,
                ('v2f', [100, 150,
                         100, 160,
                         200, 160,
                         200, 150]), 
                ('c3B', (249, 86, 86) * 4,))
    
    def render(self):#刷新并显示
        self._update_arm()#更新手臂信息
        self.switch_to()
        self.dispatch_events()
        self.dispatch_event('on_draw')
        self.flip()
    
    def on_draw(self):#刷新手臂
        self.clear()#清屏
        self.batch.draw()#画上batch里面的内容
    
    def _update_arm(self):#更新手臂信息
         (a1l, a2l) = self.arm_info['len']
         (a1r, a2r) = self.arm_info['ran']
         a1xy = self.center_coord
         a1xy_ = np.array([np.cos(a1r), np.sin(a1r)]) * a1l + a1xy
         a2xy_ = np.array([np.cos(a1r+a2r), np.sin(a1r+a2r)]) * a2l + a1xy_
         
         a1tr, a2tr = np.pi / 2 - self.arm_info['ran'][0], np.pi / 2 - self.arm_info['ran'].sum()
         xy000 = a1xy + np.array([-np.cos(a1tr), np.sin(a1tr)]) * self.bar_thc
         xy001 = a1xy + np.array([np.cos(a1tr), -np.sin(a1tr)]) * self.bar_thc
         xy011 = a1xy_ + np.array([np.cos(a1tr), -np.sin(a1tr)]) * self.bar_thc
         xy012 = a1xy_ + np.array([-np.cos(a1tr), np.sin(a1tr)]) * self.bar_thc
         
         xy100 = a1xy_ + np.array([np.cos(a2tr), -np.sin(a2tr)]) * self.bar_thc
         xy101 = a1xy_ + np.array([-np.cos(a2tr), np.sin(a2tr)]) * self.bar_thc
         xy111 = a2xy_ + np.array([-np.cos(a2tr), np.sin(a2tr)]) * self.bar_thc
         xy112 = a2xy_ + np.array([np.cos(a2tr), -np.sin(a2tr)]) * self.bar_thc
         
         self.arm1.vertices = np.concatenate((xy000, xy001, xy011, xy012))
         self.arm2.vertices = np.concatenate((xy100, xy101, xy111, xy112))
    
    def stopandclose(self):
        self.close()
        
        
#if __name__ == '__main__':
#    env = ArmEnv()
#    count = 10000
#    while 0 < count:
#        count -= 1
#        env.render()
#        env.step(env.sample_action())
#    env.close()