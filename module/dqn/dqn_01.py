# -*- coding: utf-8 -*-
"""
Created on Mon Aug  6 09:44:10 2018

@author: natasha_yang

@e-mail: ityangna0402@163.com
"""

import numpy as np
import pandas as pd
import time
from conf.conf import args

#Q-learning是一种记录行为值的方法
#选择状态
actions = [action.replace(' ', '') for action in args.get_option('dqn_01', 'ACTIONS').split(',')]
def choose_action(state, q_table):
    state_actions = q_table.iloc[state, :]#是index,就是第state行
    #如果非贪婪模式 或者 这个state对应的所有action的值都是0
    if (np.random.uniform() > args.get_option('dqn_01', 'EPSILON', 'float') or ((state_actions == 0).all())):
        #在动作中随便选择一个
        action_name = np.random.choice(actions)
    else:
        #选择当前state q-table中值最大的action
        action_name = state_actions.idxmax()
    return action_name

#创建q-table
def build_q_table(n_states, actions):
    table = pd.DataFrame(
        np.zeros((n_states, len(actions))),#6*2
        columns=actions,#列是action
    )
    #print(table)
    return table

#环境反馈
def get_env_feedback(state, action):
    if action == 'right':#向右移动
        if state == args.get_option('dqn_01', 'N_STATES', 'int') - 2:
            state_ = 'terminal'
            reward = 1
        else:
            state_ = state + 1
            reward = 0
    else:#向左移动
        reward = 0
        if state == 0:
            state_ = state#挨着墙了
        else:
            state_ = state - 1
    return state_, reward

#更新环境
def update_env(state, episode, step_counter):
    # This is how environment be updated
    env_list = ['-']*(args.get_option('dqn_01', 'N_STATES', 'int')-1) + ['T']   # '---------T' our environment
    if state == 'terminal':
        interaction = 'Episode %s: total_steps = %s' % (episode+1, step_counter)
        print('\r{}'.format(interaction), end='')
        time.sleep(2)
        print('\r                                ', end='')
    else:
        env_list[state] = 'o'
        interaction = ''.join(env_list)
        print('\r{}'.format(interaction), end='')#保证输出在同一行,且会清空当时的显示
        time.sleep(args.get_option('dqn_01', 'FRESH_TIME', 'float'))

def rl():
    q_table = build_q_table(args.get_option('dqn_01', 'N_STATES', 'int'), actions)#6,2
    for episode in range(args.get_option('dqn_01', 'MAX_EPISODES', 'int')):
        step_counter = 0
        state = 0
        is_terminated = False
        update_env(state, episode, step_counter)
        while not is_terminated:
            action = choose_action(state, q_table)
            state_, reward = get_env_feedback(state, action)
            q_predict = q_table.loc[state, action]#估计值
            if state_ != 'terminal':
                #做了这个action之后的奖励+和下一个状态可能要获得的奖励
                q_target = reward + args.get_option('dqn_01', 'GAMMA', 'float') * q_table.iloc[state_, :].max()#现实值
            else:
                q_target = reward
                is_terminated = True
            
            #现实和估计的差距
            q_table.loc[state, action] += args.get_option('dqn_01', 'ALPHA', 'float') * (q_target - q_predict)
            state = state_
            update_env(state, episode, step_counter+1)
            step_counter += 1
    return q_table

if __name__ == '__main__':
    q_table = rl()
    print('Q-table:')
    print(q_table)

#不理解环境model-free:Q-Learning+sarsa+Policy-Gradients
#理解环境model-base:想像预判
#基于概率:每种动作都可能选中只是P不同
#基于价值:选择某个价值最高的动作,连续动作无能为力Policy-Gradients
#基于概率Actor-Crictic基于价值
#回合更新 + 单步更新(更有价值)

#安装gym:pip3 install gym,全部安装:pip3 install gym[all]