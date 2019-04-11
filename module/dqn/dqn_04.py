# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 16:16:11 2019

@author: yangna

@e-mail: ityangna0402@163.com
"""

#Sarsa当前state已经想好了state对应的action,而且想好了下一个state_和下一个action_(Qlearning还没有想好下一个 action_)
from allenv import Maze
from conf.conf import args
import pandas as pd
import numpy as np

class RL(object):
    def __init__(self, actions, learning_rate=.01, reward_decay=.9, e_greedy=.9):
        self.actions = actions
        self.lr = learning_rate
        self.gamma = reward_decay
        self.epsilon = e_greedy
        self.q_table = pd.DataFrame(columns=self.actions, dtype=np.float64)
    
    def choose_action(self, observation):
        self.check_state_exist(observation)
        if np.random.uniform() < self.epsilon:
            state_action = self.q_table.loc[observation, :]
            action = np.random.choice(state_action[state_action == np.max(state_action)].index)#找到最大的index,在这些index中选
        else:
            action = np.random.choice(self.actions)#在所有的action中随机选择

        return action
    
    def learn(self, observation, action, reward, observation_):
        pass
    
    def check_state_exist(self, state):
        #print(self.q_table)
        if state not in self.q_table.index:
            self.q_table = self.q_table.append(
                pd.Series([0]*len(self.actions), index=self.q_table.columns, name=state))#新加列
        #print(self.q_table)

class SarsaTable(RL):
    def __init__(self, actions, learning_rate=.01, reward_decay=.9, e_greedy=.9):
        super(SarsaTable, self).__init__(actions, learning_rate, reward_decay, e_greedy)
    
    def learn(self, state, action, reward, state_, action_):#注意和父亲参数不一致,重写
        self.check_state_exist(state_)
        q_predict = self.q_table.loc[state, action]
        if state_ != 'terminal':
            #区别就在这儿,Q-learning是选择最大,而Sarsa是选择下一次的
            q_target = reward + self.gamma * self.q_table.loc[state_, action_]#self.q_table.loc[observation_, :].max()
        else:
            q_target = reward
        self.q_table.loc[state, action] += self.lr * (q_target - q_predict)

def update():
    for episode in range(args.get_option('dqn_04', 'MAX_EPISODES', 'int')):
        #初始化环境
        observation = env.reset()

        #Sarsa根据state观测选择行为
        action = brain.choose_action(str(observation))

        while True:
            #刷新环境
            env.render()

            #在环境中采取行为.获得下一个state_(obervation_),reward和是否终止
            observation_, reward, done = env.step(action)

            #根据下一个state(obervation_)选取下一个 action_
            action_ = brain.choose_action(str(observation_))#这是和Q-learning不同的地方他会看下一步

            #当前的和下一次的综合学习
            brain.learn(str(observation), action, reward, str(observation_), action_)

            observation = observation_
            action = action_

            if done:
                break

    env.destroy()

if __name__ == "__main__":
    env = Maze()
    brain = SarsaTable(actions=list(range(env.n_actions)))

    env.after(100, update)
    env.mainloop()