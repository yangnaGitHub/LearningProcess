# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 16:26:10 2019

@author: yangna

@e-mail: ityangna0402@163.com
"""

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

class SarsaLambdaTable(RL):
    def __init__(self, actions, learning_rate=0.01, reward_decay=0.9, e_greedy=0.9, trace_decay=0.9):
        super(SarsaLambdaTable, self).__init__(actions, learning_rate, reward_decay, e_greedy)

        self.lambda_ = trace_decay#0.9
        self.eligibility_trace = self.q_table.copy()

    def check_state_exist(self, state):
        if state not in self.q_table.index:
            to_be_append = pd.Series([0] * len(self.actions), index=self.q_table.columns, name=state)
            self.q_table = self.q_table.append(to_be_append)
            self.eligibility_trace = self.eligibility_trace.append(to_be_append)

    def learn(self, state, action, reward, state_, action_):
        self.check_state_exist(state_)
        q_predict = self.q_table.loc[state, action]
        if state_ != 'terminal':
            q_target = reward + self.gamma * self.q_table.loc[state_, action_]#sarsa
        else:
            q_target = reward
        error = q_target - q_predict

        #方法一
        # self.eligibility_trace.loc[state, action] += 1

        #方法二
        self.eligibility_trace.loc[state, :] *= 0
        self.eligibility_trace.loc[state, action] = 1

        self.q_table += self.lr * error * self.eligibility_trace
        self.eligibility_trace *= self.gamma*self.lambda_

def update():
    for episode in range(args.get_option('dqn_05', 'MAX_EPISODES', 'int')):
        observation = env.reset()

        action = brain.choose_action(str(observation))

        brain.eligibility_trace *= 0

        while True:
            env.render()

            observation_, reward, done = env.step(action)

            action_ = brain.choose_action(str(observation_))

            brain.learn(str(observation), action, reward, str(observation_), action_)

            observation = observation_
            action = action_
            
            if done:
                break

    env.destroy()

if __name__ == "__main__":
    env = Maze()
    brain = SarsaLambdaTable(actions=list(range(env.n_actions)))

    env.after(100, update)
    env.mainloop()