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

def choose_action(state, q_table):
    # This is how to choose an action
    state_actions = q_table.iloc[state, :]
    if (np.random.uniform() > args.get_option('dqn_01', 'EPSILON', 'float') or ((state_actions == 0).all())):  # act non-greedy or state-action have no value
        action_name = np.random.choice(len(args.get_option('dqn_01', 'ACTIONS').split(',')))
    else:   # act greedy
        action_name = state_actions.idxmax()    # replace argmax to idxmax as argmax means a different function in newer version of pandas
    return action_name

def build_q_table(n_states, actions):
    table = pd.DataFrame(
        np.zeros((n_states, len(actions))),     # q_table initial values
        columns=actions,    # actions's name
    )
    # print(table)    # show table
    return table

def get_env_feedback(S, A):
    # This is how agent will interact with the environment
    if A == 'right':    # move right
        if S == args.get_option('dqn_01', 'N_STATES', 'int') - 2:   # terminate
            S_ = 'terminal'
            R = 1
        else:
            S_ = S + 1
            R = 0
    else:   # move left
        R = 0
        if S == 0:
            S_ = S  # reach the wall
        else:
            S_ = S - 1
    return S_, R

def update_env(S, episode, step_counter):
    # This is how environment be updated
    env_list = ['-']*(args.get_option('dqn_01', 'N_STATES', 'int')-1) + ['T']   # '---------T' our environment
    if S == 'terminal':
        interaction = 'Episode %s: total_steps = %s' % (episode+1, step_counter)
        print('\r{}'.format(interaction), end='')
        time.sleep(2)
        print('\r                                ', end='')
    else:
        env_list[S] = 'o'
        interaction = ''.join(env_list)
        print('\r{}'.format(interaction), end='')
        time.sleep(args.get_option('dqn_01', 'FRESH_TIME', 'float'))

def rl():
    q_table = build_q_table(args.get_option('dqn_01', 'N_STATES', 'int'), len(args.get_option('dqn_01', 'ACTIONS').split(',')))#6,2
    for episode in range(args.get_option('dqn_01', 'MAX_EPISODES', 'int')):
        step_counter = 0
        S = 0
        is_terminated = False
        update_env(S, episode, step_counter)
        
        while not is_terminated:

            A = choose_action(S, q_table)
            S_, R = get_env_feedback(S, A)  # take action & get next state and reward
            q_predict = q_table.loc[S, A]
            if S_ != 'terminal':
                q_target = R + args.get_option('dqn_01', 'GAMMA', 'float') * q_table.iloc[S_, :].max()   # next state is not terminal
            else:
                q_target = R     # next state is terminal
                is_terminated = True    # terminate this episode

            q_table.loc[S, A] += args.get_option('dqn_01', 'ALPHA', 'float') * (q_target - q_predict)  # update
            S = S_  # move to next state

            update_env(S, episode, step_counter+1)
            step_counter += 1
    return q_table

if __name__ == '__main__':
    q_table = rl()
    print('\nQ-table:\n')
    print(q_table)

#不理解环境model-free:Q-Learning+sarsa+Policy-Gradients
#理解环境model-base:想像预判
#基于概率:每种动作都可能选中只是P不同
#基于价值:选择某个价值最高的动作,连续动作无能为力Policy-Gradients
#基于概率Actor-Crictic基于价值
#回合更新 + 单步更新(更有价值)