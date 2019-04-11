# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 14:59:17 2019

@author: yangna

@e-mail: ityangna0402@163.com
"""

#DQN是基于Q-learning的,Q-learning会有Qmax,Qmax会导致Q现实中过估计
#Double DQN是用来解决过估计的
#如果输出的DQN的Q值超级大,这就是出现了过估计

import numpy as np
import tensorflow as tf

np.random.seed(1)
tf.set_random_seed(1)

class DoubleDQN:
    def __init__(self,
                 n_actions,#11
                 n_features,#3
                 learning_rate=0.005, reward_decay=0.9, e_greedy=0.9, replace_target_iter=200, memory_size=3000,
                 batch_size=32, e_greedy_increment=None, output_graph=False, double_q=True, sess=None):
        
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

        self.double_q = double_q#是否使用double_dqn

        self.learn_step_counter = 0
        self.memory = np.zeros((self.memory_size, n_features*2+2))
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

            with tf.variable_scope('l2'):
                w2 = tf.get_variable('w2', [n_l1, self.n_actions], initializer=w_initializer, collections=c_names)
                b2 = tf.get_variable('b2', [1, self.n_actions], initializer=b_initializer, collections=c_names)
                out = tf.matmul(l1, w2) + b2
            return out
        
        self.s = tf.placeholder(tf.float32, [None, self.n_features], name='s')
        self.q_target = tf.placeholder(tf.float32, [None, self.n_actions], name='Q_target')
        with tf.variable_scope('eval_net'):
            c_names, n_l1, w_initializer, b_initializer = ['eval_net_params', tf.GraphKeys.GLOBAL_VARIABLES], 20, tf.random_normal_initializer(0., 0.3), tf.constant_initializer(0.1)
            self.q_eval = build_layers(self.s, c_names, n_l1, w_initializer, b_initializer)

        with tf.variable_scope('loss'):
            self.loss = tf.reduce_mean(tf.squared_difference(self.q_target, self.q_eval))
        with tf.variable_scope('train'):
            self._train_op = tf.train.RMSPropOptimizer(self.lr).minimize(self.loss)

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
        actions_value = self.sess.run(self.q_eval, feed_dict={self.s: observation})#eval_net获取action的reward
        action = np.argmax(actions_value)#选取最大

        if not hasattr(self, 'q'):
            self.q = []
            self.running_q = 0
        #0.01x_1 => 0.99*0.01x_1+0.01x_2 => 0.99*0.99*0.11x_1+0.01*0.99*x_2+0.01x_3
        #0.01x_1 => 0.0099x_1+0.01x_2 => 0.009801x_1+0.0099x_2+0.01x_3
        #之前的action_value有影响,越远就影响越小,目的何在,用于显示,平滑??
        self.running_q = self.running_q*0.99 + 0.01 * np.max(actions_value)
        self.q.append(self.running_q)

        if np.random.uniform() > self.epsilon:
            action = np.random.randint(0, self.n_actions)
        return action

    def learn(self):
        if self.learn_step_counter % self.replace_target_iter == 0:
            self.sess.run(self.replace_target_op)
            print('\ntarget_params_replaced\n')

        if self.memory_counter > self.memory_size:
            sample_index = np.random.choice(self.memory_size, size=self.batch_size)
        else:
            sample_index = np.random.choice(self.memory_counter, size=self.batch_size)
        batch_memory = self.memory[sample_index, :]

        q_next, q_eval4next = self.sess.run([self.q_next, self.q_eval],
                                            feed_dict={self.s_: batch_memory[:, -self.n_features:],
                                                       self.s: batch_memory[:, -self.n_features:]})#q_eval4next使用的是s_作为输入
        q_eval = self.sess.run(self.q_eval, {self.s: batch_memory[:, :self.n_features]})##q_eval使用的是s作为输入

        q_target = q_eval.copy()

        batch_index = np.arange(self.batch_size, dtype=np.int32)
        eval_act_index = batch_memory[:, self.n_features].astype(int)
        reward = batch_memory[:, self.n_features + 1]

        if self.double_q:#double DQN
            max_act4next = np.argmax(q_eval4next, axis=1)#行上选择最大action value最大的index
            selected_q_next = q_next[batch_index, max_act4next]#q_next中选择q_eval4next每行最大action value最大的index
        else:
            selected_q_next = np.max(q_next, axis=1)#选择值最大的
        #所以区别在于算q_target的时候的下一步的reward的选取规则,一个是q_eval4next上最大的action对应的值,一个是直接是最大

        q_target[batch_index, eval_act_index] = reward + self.gamma * selected_q_next

        _, self.cost = self.sess.run([self._train_op, self.loss],
                                     feed_dict={self.s: batch_memory[:, :self.n_features],
                                                self.q_target: q_target})
        self.cost_his.append(self.cost)

        self.epsilon = self.epsilon + self.epsilon_increment if self.epsilon < self.epsilon_max else self.epsilon_max
        self.learn_step_counter += 1

import matplotlib.pyplot as plt
import gym
from conf.conf import args

env = gym.make('Pendulum-v0')
env = env.unwrapped#取消限制
env.seed(1)#回合的方差比较大,所以选一个好点的随机种子

sess = tf.Session()
with tf.variable_scope('Natural_DQN'):
    natural_DQN = DoubleDQN(n_actions=args.get_option('dqn_07', 'ACTION_SPACE', 'int'), n_features=3,
                            memory_size=args.get_option('dqn_07', 'MEMORY_SIZE', 'int'), e_greedy_increment=0.001, double_q=False, sess=sess)
with tf.variable_scope('Double_DQN'):
    double_DQN = DoubleDQN(n_actions=args.get_option('dqn_07', 'ACTION_SPACE', 'int'), n_features=3,
                           memory_size=args.get_option('dqn_07', 'MEMORY_SIZE', 'int'), e_greedy_increment=0.001, double_q=True, sess=sess, output_graph=True)
sess.run(tf.global_variables_initializer())

def train(RL):
    total_steps = 0
    observation = env.reset()
    while True:
        action = RL.choose_action(observation)
        #(action-5)/(10/4)
        f_action = (action-(args.get_option('dqn_07', 'ACTION_SPACE', 'int')-1)/2)/((args.get_option('dqn_07', 'ACTION_SPACE', 'int')-1)/4)
        observation_, reward, done, info = env.step(np.array([f_action]))

        reward /= 10
        RL.store_transition(observation, action, reward, observation_)

        if total_steps > args.get_option('dqn_07', 'MEMORY_SIZE', 'int'):#只要是存满3000笔就开始训练,每次都训练
            RL.learn()

        if total_steps - args.get_option('dqn_07', 'MEMORY_SIZE', 'int') > 20000:
            break

        observation = observation_
        total_steps += 1
    return RL.q

q_natural = train(natural_DQN)
q_double = train(double_DQN)

plt.plot(np.array(q_natural), c='r', label='natural')
plt.plot(np.array(q_double), c='b', label='double')
plt.legend(loc='best')
plt.ylabel('Q eval')
plt.xlabel('training steps')
plt.grid()
plt.show()