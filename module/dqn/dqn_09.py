# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 14:59:20 2019

@author: yangna

@e-mail: ityangna0402@163.com
"""

#Dueling DQN:将每个动作的Q拆分成了state的Value加上每个动作在这个state上的Advantage
#原因:有种情况是无论做什么动作,对下一个state都没有多大的影响(比如自动驾驶等)
import numpy as np
import tensorflow as tf

np.random.seed(1)
tf.set_random_seed(1)

class DuelingDQN:
    def __init__(self, n_actions, n_features, learning_rate=0.001, reward_decay=0.9, e_greedy=0.9, replace_target_iter=200,
                 memory_size=500, batch_size=32, e_greedy_increment=None, output_graph=False, dueling=True, sess=None):
        self.n_actions = n_actions
        self.n_features = n_features
        self.lr = learning_rate
        self.gamma = reward_decay
        self.epsilon_max = e_greedy
        self.replace_target_iter = replace_target_iter
        self.memory_size = memory_size
        self.batch_size = batch_size
        self.epsilon_increment = e_greedy_increment
        self.epsilon = 0 if e_greedy_increment is not None else self.epsilon_max

        self.dueling = dueling
        
        self.learn_step_counter = 0
        self.memory = np.zeros((self.memory_size, n_features*2+2))#准备要使用的空间
        self._build_net()
        t_params = tf.get_collection('target_net_params')
        e_params = tf.get_collection('eval_net_params')
        self.replace_target_op = [tf.assign(t, e) for t, e in zip(t_params, e_params)]

        if sess is None:
            self.sess = tf.Session()
            self.sess.run(tf.global_variables_initializer())
        else:
            self.sess = sess
        if output_graph:
            tf.summary.FileWriter('log/', self.sess.graph)
        self.cost_his = []

    def _build_net(self):
        def build_layers(s, c_names, n_l1, w_initializer, b_initializer):
            with tf.variable_scope('l1'):
                w1 = tf.get_variable('w1', [self.n_features, n_l1], initializer=w_initializer, collections=c_names)
                b1 = tf.get_variable('b1', [1, n_l1], initializer=b_initializer, collections=c_names)
                l1 = tf.nn.relu(tf.matmul(s, w1) + b1)
            
            #却别在于out的计算
            if self.dueling:
                #Dueling DQN,l1->Value+Advantage
                with tf.variable_scope('Value'):
                    w2 = tf.get_variable('w2', [n_l1, 1], initializer=w_initializer, collections=c_names)
                    b2 = tf.get_variable('b2', [1, 1], initializer=b_initializer, collections=c_names)
                    self.V = tf.matmul(l1, w2) + b2#l1作为输入(self.n_features,1)

                with tf.variable_scope('Advantage'):
                    w2 = tf.get_variable('w2', [n_l1, self.n_actions], initializer=w_initializer, collections=c_names)
                    b2 = tf.get_variable('b2', [1, self.n_actions], initializer=b_initializer, collections=c_names)
                    self.A = tf.matmul(l1, w2) + b2#l1作为输入(self.n_features,self.n_actions)

                with tf.variable_scope('Q'):
                    #计算张量tensor沿着指定的数轴(tensor的某一维度)上的的平均值
                    #按行求均值(batch,),keep_dims保持维度(batch,1)
                    #不让A直接学成了Q减掉A的均值
                    out = self.V + (self.A - tf.reduce_mean(self.A, axis=1, keep_dims=True))#真正的输出,Q=V(s)+A(s,a)
            else:
                with tf.variable_scope('Q'):
                    w2 = tf.get_variable('w2', [n_l1, self.n_actions], initializer=w_initializer, collections=c_names)
                    b2 = tf.get_variable('b2', [1, self.n_actions], initializer=b_initializer, collections=c_names)
                    out = tf.matmul(l1, w2) + b2

            return out

        #eval_net
        self.s = tf.placeholder(tf.float32, [None, self.n_features], name='s')
        self.q_target = tf.placeholder(tf.float32, [None, self.n_actions], name='Q_target')
        with tf.variable_scope('eval_net'):
            c_names, n_l1, w_initializer, b_initializer = ['eval_net_params', tf.GraphKeys.GLOBAL_VARIABLES], 20, tf.random_normal_initializer(0., 0.3), tf.constant_initializer(0.1)
            self.q_eval = build_layers(self.s, c_names, n_l1, w_initializer, b_initializer)

        with tf.variable_scope('loss'):
            self.loss = tf.reduce_mean(tf.squared_difference(self.q_target, self.q_eval))
        with tf.variable_scope('train'):
            self._train_op = tf.train.RMSPropOptimizer(self.lr).minimize(self.loss)

        #target_net
        self.s_ = tf.placeholder(tf.float32, [None, self.n_features], name='s_')
        with tf.variable_scope('target_net'):
            c_names = ['target_net_params', tf.GraphKeys.GLOBAL_VARIABLES]
            self.q_next = build_layers(self.s_, c_names, n_l1, w_initializer, b_initializer)

    def store_transition(self, s, a, r, s_):
        if not hasattr(self, 'memory_counter'):
            self.memory_counter = 0
        transition = np.hstack((s, [a, r], s_))
        index = self.memory_counter % self.memory_size
        self.memory[index, :] = transition
        self.memory_counter += 1

    def choose_action(self, observation):
        observation = observation[np.newaxis, :]
        if np.random.uniform() < self.epsilon:
            actions_value = self.sess.run(self.q_eval, feed_dict={self.s: observation})
            action = np.argmax(actions_value)
        else:
            action = np.random.randint(0, self.n_actions)
        return action

    def learn(self):
        if self.learn_step_counter % self.replace_target_iter == 0:
            self.sess.run(self.replace_target_op)
            print('\ntarget_params_replaced\n')

        sample_index = np.random.choice(self.memory_size, size=self.batch_size)
        batch_memory = self.memory[sample_index, :]

        q_next = self.sess.run(self.q_next, feed_dict={self.s_: batch_memory[:, -self.n_features:]})
        q_eval = self.sess.run(self.q_eval, {self.s: batch_memory[:, :self.n_features]})

        q_target = q_eval.copy()

        batch_index = np.arange(self.batch_size, dtype=np.int32)
        eval_act_index = batch_memory[:, self.n_features].astype(int)
        reward = batch_memory[:, self.n_features + 1]

        q_target[batch_index, eval_act_index] = reward + self.gamma * np.max(q_next, axis=1)

        _, self.cost = self.sess.run([self._train_op, self.loss],
                                     feed_dict={self.s: batch_memory[:, :self.n_features],
                                                self.q_target: q_target})
        self.cost_his.append(self.cost)

        self.epsilon = self.epsilon + self.epsilon_increment if self.epsilon < self.epsilon_max else self.epsilon_max
        self.learn_step_counter += 1

import gym
import matplotlib.pyplot as plt
from conf.conf import args

def train(RL):
    acc_r = [0]
    total_steps = 0
    observation = env.reset()
    while True:
        action = RL.choose_action(observation)

        f_action = (action-(args.get_option('dqn_09', 'ACTION_SPACE', 'int')-1)/2)/((args.get_option('dqn_09', 'ACTION_SPACE', 'int')-1)/4)
        observation_, reward, done, info = env.step(np.array([f_action]))

        reward /= 10
        acc_r.append(reward + acc_r[-1])

        RL.store_transition(observation, action, reward, observation_)

        if total_steps > args.get_option('dqn_09', 'MEMORY_SIZE', 'int'):#从3000轮开始训练,就是数据填满开始训练
            RL.learn()

        if total_steps-args.get_option('dqn_09', 'MEMORY_SIZE', 'int') > 15000:#最多训练15000次就停止训练
            break

        observation = observation_
        total_steps += 1
    return RL.cost_his, acc_r

if __name__ == '__main__':
    env = gym.make('Pendulum-v0')
    env = env.unwrapped
    env.seed(1)

    sess = tf.Session()
    with tf.variable_scope('natural'):
        natural_DQN = DuelingDQN(n_actions=args.get_option('dqn_09', 'ACTION_SPACE', 'int'), n_features=3,
                                 memory_size=args.get_option('dqn_09', 'MEMORY_SIZE', 'int'), e_greedy_increment=0.001, sess=sess, dueling=False)

    with tf.variable_scope('dueling'):
        dueling_DQN = DuelingDQN(n_actions=args.get_option('dqn_09', 'ACTION_SPACE', 'int'), n_features=3,
                                 memory_size=args.get_option('dqn_09', 'MEMORY_SIZE', 'int'), e_greedy_increment=0.001, sess=sess, dueling=True, output_graph=True)
    sess.run(tf.global_variables_initializer())

    c_natural, r_natural = train(natural_DQN)
    c_dueling, r_dueling = train(dueling_DQN)

    plt.figure(1)
    plt.plot(np.array(c_natural), c='r', label='natural')
    plt.plot(np.array(c_dueling), c='b', label='dueling')
    plt.legend(loc='best')
    plt.ylabel('cost')
    plt.xlabel('training steps')
    plt.grid()

    plt.figure(2)
    plt.plot(np.array(r_natural), c='r', label='natural')
    plt.plot(np.array(r_dueling), c='b', label='dueling')
    plt.legend(loc='best')
    plt.ylabel('accumulated reward')
    plt.xlabel('training steps')
    plt.grid()

    plt.show()