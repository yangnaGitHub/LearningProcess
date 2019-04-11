# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 14:59:18 2019

@author: yangna

@e-mail: ityangna0402@163.com
"""

#DQN with Prioritized Replay:会重视少量的,但值得学习的样本
import numpy as np
import tensorflow as tf

np.random.seed(1)
tf.set_random_seed(1)

#是二叉树结构,树叶存储每个样本的优先级值,每个节点的值是两个儿子的和,所以root是所有树叶的值的和
#        12=(5+7)
#  5=(1+4)     7=(3+4)
#1    4     3     4
#(0-1)(1-5)(5-8)(8-11)
#抽样的时候用root的值/batch,分成batch个区间,比如上面要分成3个batch=>优先级的区间划分[0-4][4-8][8-12]
#在每个区间中随机的选取一个数值
  #值11和左边比大于5,走右边,值修改为11-5=6,6和7左边的比较大于3,值修改为6-3,所以选择4当做这次选到的优先级和对应的数据

class SumTree(object):
    data_pointer = 0

    def __init__(self, capacity):
        self.capacity = capacity
        self.tree = np.zeros(2 * capacity - 1)#2*10000-1=19999#存储所有record的优先级
        #[--------------存储树枝节点-------------][-----------存储树叶节点------------------]
        #           size: capacity - 1                       size: capacity
        #注意此处是dtype=object所以可以存储10个数值,这种用法要学会,使用1维的数组存储object对象
        self.data = np.zeros(capacity, dtype=object)#存储所有的record,10000
        #[--------------保存记录-----------------]
        #           size: capacity

    def add(self, p, data):
        tree_idx = self.data_pointer + self.capacity - 1
        self.data[self.data_pointer] = data
        self.update(tree_idx, p)

        self.data_pointer += 1
        if self.data_pointer >= self.capacity:#循环保存
            self.data_pointer = 0

    def update(self, tree_idx, p):
        change = p - self.tree[tree_idx]
        self.tree[tree_idx] = p
        while tree_idx != 0:
            tree_idx = (tree_idx - 1) // 2#修改父亲的优先级
            self.tree[tree_idx] += change

    def get_leaf(self, v):
        """
        Tree structure and array storage:
        Tree index:
             0         -> storing priority sum
            / \
          1     2
         / \   / \
        3   4 5   6    -> storing priority for transitions
        Array type for storing:
        [0,1,2,3,4,5,6]
        """
        parent_idx = 0
        while True:#遍历
            cl_idx = 2 * parent_idx + 1#左孩子
            cr_idx = cl_idx + 1#右孩子
            if cl_idx >= len(self.tree):#2*capacity-1
                leaf_idx = parent_idx
                break
            else:
                if v <= self.tree[cl_idx]:#如果值小于等于左孩子就取左孩子
                    parent_idx = cl_idx
                else:
                    v -= self.tree[cl_idx]#如果大于左孩子,就减去左孩子的值作为新的值,并取右孩子
                    parent_idx = cr_idx

        data_idx = leaf_idx - self.capacity + 1
        return leaf_idx, self.tree[leaf_idx], self.data[data_idx]
    
    #@property装饰器:负责吧一个方法变成属性调用
    @property
    def total_p(self):
        return self.tree[0]


class Memory(object):
    epsilon = 0.01
    alpha = 0.6
    beta = 0.4
    beta_increment_per_sampling = 0.001
    abs_err_upper = 1.

    def __init__(self, capacity):
        self.tree = SumTree(capacity)

    def store(self, transition):
        max_p = np.max(self.tree.tree[-self.tree.capacity:])#tree所有的树叶中取最大
        if max_p == 0:
            max_p = self.abs_err_upper
        self.tree.add(max_p, transition)#为啥是max_p,这是所为何
    
    #就是将优先级划分为n个区域,每个局域按照均匀分布采样一个样本
    def sample(self, n):#n=batch=32
        #b_idx(32,),b_memory(32*10[object的size]),ISWeights(32*1)
        b_idx, b_memory, ISWeights = np.empty((n,), dtype=np.int32), np.empty((n, self.tree.data[0].size)), np.empty((n, 1))
        pri_seg = self.tree.total_p / n#方法当做属性用(装饰器),总和分成batch个区
        self.beta = np.min([1., self.beta + self.beta_increment_per_sampling])#最大取1,从0.4开始,每次递增0.001

        min_prob = np.min(self.tree.tree[-self.tree.capacity:]) / self.tree.total_p#优先级中最小的数值/总和
        for i in range(n):
            a, b = pri_seg * i, pri_seg * (i + 1)#确定分区
            v = np.random.uniform(a, b)#均匀分布[a,b)中随机采样,每个分区获得一个样本
            idx, p, data = self.tree.get_leaf(v)
            prob = p / self.tree.total_p#p:获取的样本的优先级
            ISWeights[i, 0] = np.power(prob/min_prob, -self.beta)#prob/min_prob**-self.beta
            b_idx[i], b_memory[i, :] = idx, data
        return b_idx, b_memory, ISWeights

    def batch_update(self, tree_idx, abs_errors):
        abs_errors += self.epsilon
        clipped_errors = np.minimum(abs_errors, self.abs_err_upper)
        ps = np.power(clipped_errors, self.alpha)
        for ti, p in zip(tree_idx, ps):
            self.tree.update(ti, p)


class DQNPrioritizedReplay:
    def __init__(self, n_actions, n_features, learning_rate=0.005, reward_decay=0.9,
                 e_greedy=0.9, replace_target_iter=500, memory_size=10000, batch_size=32,
                 e_greedy_increment=None, output_graph=False, prioritized=True, sess=None):
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
        self.prioritized = prioritized
        self.learn_step_counter = 0
        self._build_net()
        
        t_params = tf.get_collection('target_net_params')
        e_params = tf.get_collection('eval_net_params')
        self.replace_target_op = [tf.assign(t, e) for t, e in zip(t_params, e_params)]

        if self.prioritized:
            self.memory = Memory(capacity=memory_size)
        else:
            self.memory = np.zeros((self.memory_size, n_features*2+2))#申请memory

        if sess is None:
            self.sess = tf.Session()
            self.sess.run(tf.global_variables_initializer())
        else:
            self.sess = sess

        if output_graph:
            tf.summary.FileWriter('log/', self.sess.graph)

        self.cost_his = []

    def _build_net(self):
        def build_layers(s, c_names, n_l1, w_initializer, b_initializer, trainable):
            with tf.variable_scope('l1'):
                w1 = tf.get_variable('w1', [self.n_features, n_l1], initializer=w_initializer, collections=c_names, trainable=trainable)
                b1 = tf.get_variable('b1', [1, n_l1], initializer=b_initializer, collections=c_names,  trainable=trainable)
                l1 = tf.nn.relu(tf.matmul(s, w1) + b1)

            with tf.variable_scope('l2'):
                w2 = tf.get_variable('w2', [n_l1, self.n_actions], initializer=w_initializer, collections=c_names,  trainable=trainable)
                b2 = tf.get_variable('b2', [1, self.n_actions], initializer=b_initializer, collections=c_names,  trainable=trainable)
                out = tf.matmul(l1, w2) + b2
            return out

        #eval_net
        self.s = tf.placeholder(tf.float32, [None, self.n_features], name='s')
        self.q_target = tf.placeholder(tf.float32, [None, self.n_actions], name='Q_target')
        if self.prioritized:
            self.ISWeights = tf.placeholder(tf.float32, [None, 1], name='IS_weights')
        with tf.variable_scope('eval_net'):
            c_names, n_l1, w_initializer, b_initializer = ['eval_net_params', tf.GraphKeys.GLOBAL_VARIABLES], 20, tf.random_normal_initializer(0., 0.3), tf.constant_initializer(0.1)
            self.q_eval = build_layers(self.s, c_names, n_l1, w_initializer, b_initializer, True)

        with tf.variable_scope('loss'):
            if self.prioritized:
                self.abs_errors = tf.reduce_sum(tf.abs(self.q_target - self.q_eval), axis=1)#计算差的绝对值的和
                self.loss = tf.reduce_mean(self.ISWeights * tf.squared_difference(self.q_target, self.q_eval))
            else:
                self.loss = tf.reduce_mean(tf.squared_difference(self.q_target, self.q_eval))
        with tf.variable_scope('train'):
            self._train_op = tf.train.RMSPropOptimizer(self.lr).minimize(self.loss)

        #target_net
        self.s_ = tf.placeholder(tf.float32, [None, self.n_features], name='s_')
        with tf.variable_scope('target_net'):
            c_names = ['target_net_params', tf.GraphKeys.GLOBAL_VARIABLES]
            self.q_next = build_layers(self.s_, c_names, n_l1, w_initializer, b_initializer, False)

    def store_transition(self, s, a, r, s_):
        transition = np.hstack((s, [a, r], s_))
        if self.prioritized:
            self.memory.store(transition)
        else:
            if not hasattr(self, 'memory_counter'):
                self.memory_counter = 0
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

        if self.prioritized:
            tree_idx, batch_memory, ISWeights = self.memory.sample(self.batch_size)
        else:
            sample_index = np.random.choice(self.memory_size, size=self.batch_size)
            batch_memory = self.memory[sample_index, :]

        q_next, q_eval = self.sess.run([self.q_next, self.q_eval],
                                       feed_dict={self.s_: batch_memory[:, -self.n_features:],
                                                  self.s: batch_memory[:, :self.n_features]})

        q_target = q_eval.copy()
        batch_index = np.arange(self.batch_size, dtype=np.int32)
        eval_act_index = batch_memory[:, self.n_features].astype(int)
        reward = batch_memory[:, self.n_features + 1]

        q_target[batch_index, eval_act_index] = reward + self.gamma * np.max(q_next, axis=1)

        if self.prioritized:
            _, abs_errors, self.cost = self.sess.run([self._train_op, self.abs_errors, self.loss],
                                                     feed_dict={self.s: batch_memory[:, :self.n_features],
                                                                self.q_target: q_target,
                                                                self.ISWeights: ISWeights})
            self.memory.batch_update(tree_idx, abs_errors)#batch中的要更新优先级
        else:
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
    total_steps = 0
    steps = []
    episodes = []
    for i_episode in range(20):
        observation = env.reset()
        while True:
            action = RL.choose_action(np.array(observation))

            observation_, reward, done, info = env.step(action)

            if done:
                reward = 10

            RL.store_transition(observation, action, reward, observation_)

            if total_steps > args.get_option('dqn_07', 'MEMORY_SIZE', 'int'):#从10000步开始训练
                RL.learn()

            if done:
                print('episode ', i_episode, ' finished')
                steps.append(total_steps)
                episodes.append(i_episode)
                break

            observation = observation_
            total_steps += 1
    return np.vstack((episodes, steps))#第一行是episodes,第二行是steps

if __name__ == '__main__':
    env = gym.make('MountainCar-v0')
    env = env.unwrapped
    env.seed(21)
    sess = tf.Session()
    with tf.variable_scope('natural_DQN'):
        RL_natural = DQNPrioritizedReplay(n_actions=3, n_features=2, memory_size=args.get_option('dqn_08', 'MEMORY_SIZE', 'int'),
                                          e_greedy_increment=0.00005, sess=sess, prioritized=False)

    with tf.variable_scope('DQN_with_prioritized_replay'):
        RL_prio = DQNPrioritizedReplay(n_actions=3, n_features=2, memory_size=args.get_option('dqn_08', 'MEMORY_SIZE', 'int'),
                                       e_greedy_increment=0.00005, sess=sess, prioritized=True, output_graph=True)
    sess.run(tf.global_variables_initializer())
    
    his_natural = train(RL_natural)
    his_prio = train(RL_prio)

    plt.plot(his_natural[0, :], his_natural[1, :] -his_natural[1, 0], c='b', label='natural DQN')
    plt.plot(his_prio[0, :], his_prio[1, :] -his_prio[1, 0], c='r', label='DQN with prioritized replay')
    plt.legend(loc='best')
    plt.ylabel('total training time')
    plt.xlabel('episode')
    plt.grid()
    plt.show()