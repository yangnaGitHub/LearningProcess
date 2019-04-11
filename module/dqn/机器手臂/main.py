# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 13:49:40 2019

@author: yangna

@e-mail: ityangna0402@163.com
"""

from armenv import ArmEnv
from alldqn import DDPG
MAX_EPISODES = 500
MAX_EP_STEPS = 200

env = ArmEnv()
state_shape = env.state_shape
action_shape = env.action_shape
action_threshold = env.action_threshold

dqn = DDPG(action_shape, state_shape, action_threshold)

for _ in range(MAX_EPISODES):
    state = env.reset()
    for index in range(MAX_EP_STEPS):
        env.render()#环境渲染
        action = dqn.choose_action(state)
        new_s, reward, done = env.step(action)
        
        dqn.store_transition(state, action, reward, new_s)#将数据存放在开辟的空间中
        if dqn.memory_full:#如果空间满了就学习
            dqn.learn()
        if done:
            break
        state = new_s
#调用的主体出来
#ArmEnv:
#    reset()
#    render()
#    step(action)
#    state_shape
#    action_shape
#    action_threshold
#DDPG:
#    choose_action(state)
#    learn()
#    store_transition(state, action, reward, new_s)
#    memory_full