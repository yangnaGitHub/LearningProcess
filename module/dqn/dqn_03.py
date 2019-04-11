# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 18:13:26 2019

@author: natasha_yang

@e-mail: ityangna0402@163.com
"""

from allenv import Maze
from conf.conf import args
import pandas as pd
import numpy as np

class QLearningTable(object):
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
    
    def learn(self, observation, action, reward, observation_):#Q-learning的算法做的
        self.check_state_exist(observation_)
        q_predict = self.q_table.loc[observation, action]
        if observation_ != 'terminal':
            q_target = reward + self.gamma * self.q_table.loc[observation_, :].max()
        else:
            q_target = reward
        self.q_table.loc[observation, action] += self.lr * (q_target - q_predict)
    
    def check_state_exist(self, state):
        print(self.q_table)
        if state not in self.q_table.index:
            self.q_table = self.q_table.append(
                pd.Series([0]*len(self.actions), index=self.q_table.columns, name=state))#新加列
        print(self.q_table)

def update():
    for episode in range(args.get_option('dqn_03', 'MAX_EPISODES', 'int')):
        observation = env.reset()
        while True:
            env.render()
            action = brain.choose_action(str(observation))
            observation_, reward, done = env.step(action)
            brain.learn(str(observation), action, reward, str(observation_))
            observation = observation_
            if done:
                break
    env.destroy()

if __name__ == '__main__':
    env = Maze()
    brain = QLearningTable(actions=list(range(env.n_actions)))
    env.after(100, update)
    env.mainloop()