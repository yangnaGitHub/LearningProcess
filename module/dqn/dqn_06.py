# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 08:47:13 2019

@author: yangna

@e-mail: ityangna0402@163.com
"""

from allenv import Maze
from conf.conf import args
import numpy as np
import tensorflow as tf

np.random.seed(1)
tf.set_random_seed(1)
class DeepQNetwork(object):
    def __init__(self, n_actions, n_features, learning_rate=0.01, reward_decay=0.9, e_greedy=0.9,#4,4
                 replace_target_iter=300,#200
                 memory_size=500, batch_size=32,#2000,32
                 e_greedy_increment=None,
                 output_graph=False):
        self.n_actions = n_actions
        self.n_features = n_features
        self.lr = learning_rate
        self.gamma = reward_decay
        self.epsilon_max = e_greedy
        self.replace_target_iter = replace_target_iter
        self.memory_size = memory_size
        self.batch_size = batch_size
        self.epsilon_increment = e_greedy_increment
        self.epsilon = 0 if e_greedy_increment is not None else self.epsilon_max#0.9对贪婪因子做一步处理
        self.learn_step_counter = 0#记录
        self.memory = np.zeros((self.memory_size, n_features * 2 + 2))#申请存储空间2000*[4*2+2=10]=>observation, action, reward, observation_
        self._build_net()#构建网络

        t_params = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope='target_net')
        e_params = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope='eval_net')

        with tf.variable_scope('hard_replacement'):
            self.target_replace_op = [tf.assign(t, e) for t, e in zip(t_params, e_params)]#t_params更新为e_params的参数的操作

        self.sess = tf.Session()

        if output_graph:
            #tensorboard
            tf.summary.FileWriter('log/', self.sess.graph)

        self.sess.run(tf.global_variables_initializer())
        self.cost_his = []

    def _build_net(self):
        #输入
        self.s = tf.placeholder(tf.float32, [None, self.n_features], name='s')#batch*4当前状态
        self.s_ = tf.placeholder(tf.float32, [None, self.n_features], name='s_')#batch*4执行action一步之后到达的新状态
        self.r = tf.placeholder(tf.float32, [None, ], name='r')#batch,这一步获得的奖励
        self.a = tf.placeholder(tf.int32, [None, ], name='a')#batch,这一步
        
        #参数初始化
        #random_normal_initializer用正态分布产生张量的初始化器,mean=0.,std=0.3
        #constant_initializer初始化成常量的初始化器
        w_initializer, b_initializer = tf.random_normal_initializer(0., 0.3), tf.constant_initializer(0.1)
#        self.W = tf.Variable(
#                        tf.random_uniform([self.args.vocab_size, self.get_option('embedding', 'embedding_size', 'int')], -1.0, 1.0),#vocab_size(build_vocab_size 最大5000字) * embedding_size [-1, 1]
#                        name="W")

        #eval网络
        with tf.variable_scope('eval_net'):#trainable=True
            #tf.layers.dense全连接层,相当于添加一个层
            #self.s作为input[batch*4]=>全连接层输出是20[4*20]=>batch*20
            #eval_1_W = tf.Variable(tf.random_uniform([self.n_features, 20], 0., 0.3), name='eval_1_W')
            #eval_1_b = tf.Variable(tf.constant(0.1, shape=[20]), name='eval_1_b')
            #eval_1 = tf.nn.relu(tf.matmul(self.s, eval_1_W) + eval_1_b)
            eval_1 = tf.layers.dense(self.s, 20, tf.nn.relu, kernel_initializer=w_initializer, bias_initializer=b_initializer, name='eval_1')
            self.q_eval = tf.layers.dense(eval_1, self.n_actions, kernel_initializer=w_initializer, bias_initializer=b_initializer, name='q_eval')#*(batch*4)

        with tf.variable_scope('q_eval'):
            #stack,axis=1=>[0,1,2],[4,5,6]=>[[0,4],[1,5],[2,6]]
            ##stack,axis=0=>[0,1,2],[4,5,6]=>[[0,1,2],[4,5,6]]
            a_indices = tf.stack([tf.range(tf.shape(self.a)[0], dtype=tf.int32), self.a], axis=1)#(batch*2)=>每一行[index,action_value]
            #gather:按照索引提取得到新的向量,提取一维的矩阵逻辑变换
            #gather_nd:提取多维度的矩阵逻辑操作
            #(batch*4)按照(batch*2)提取值
            #q_eval每一行是4个action的reward值,获取a中指定的action的reward的值
            self.q_eval_wrt_a = tf.gather_nd(params=self.q_eval, indices=a_indices)#根据当前state计算出action的reward值

        #target网络,用来算loss的,这儿不更新参数和实时学习更新参数的平方差最小的目的何在???
        #固定住神经网络的参数,target_net是eval_net的一个历史版本,对做了某个操作之后的state建模
        with tf.variable_scope('target_net'):#trainable=False
            target_1 = tf.layers.dense(self.s_, 20, tf.nn.relu, kernel_initializer=w_initializer, bias_initializer=b_initializer, name='target_1')
            self.q_next = tf.layers.dense(target_1, self.n_actions, kernel_initializer=w_initializer, bias_initializer=b_initializer, name='q_next')

        with tf.variable_scope('q_target'):
            #reduce_max压缩求最大值,用于降维,axis=1是按照行=>4个action的后续的奖励中选择一个最大的(batch*1)
            #计算最终的奖励
            q_target = self.r + self.gamma * tf.reduce_max(self.q_next, axis=1, name='Qmax_s_')#根据做了action之后的state计算reward
            #阻挡节点的梯度,这个节点就无法在BP
            self.q_target = tf.stop_gradient(q_target)
        
        #self.q_target,self.q_eval_wrt_a之间的平方差最小
        #学习的时候由于target_net中的stop_gradient,所以不会对target_net中进行BP,所以target_net中的参数不会变动
        #直到学习了200次之后才会让target_net的参数更新成eval_net中的参数
        #根据当前state,eval_net会给出每个action的后续的reward
        with tf.variable_scope('loss'):
            self.loss = tf.reduce_mean(tf.squared_difference(self.q_target, self.q_eval_wrt_a, name='TD_error'))#平方差求均值
        
        with tf.variable_scope('train'):
            self._train_op = tf.train.RMSPropOptimizer(self.lr).minimize(self.loss)#优化的目的是啥,怎么优化

    def store_transition(self, s, a, r, s_):
        if not hasattr(self, 'memory_counter'):#没有memory_counter这个变量
            self.memory_counter = 0#定义并且初始化
        #np.hstack((data1, data2))#水平 20*10, 20*100 ==> 20*110
        #组合成要保存的数据格式
        transition = np.hstack((s, [a, r], s_))#(4,)[(1,)(1,)](4,)=>(10,)[s:(0-3)a:(4)r:(5)s_:(6-9)]
        index = self.memory_counter % self.memory_size#循环保存,溢出重头开始保存
        self.memory[index, :] = transition
        self.memory_counter += 1

    def choose_action(self, observation):
        #[1, 2, 3]=>[np.newaxis, :]=>[[1, 2, 3]]
        #[1, 2, 3]=>[:, np.newaxis]=>[[1],[2],[3]]
        observation = np.array(observation)[np.newaxis, :]#(4,)=>(1,4)

        if np.random.uniform() < self.epsilon:
            #batch=1=>(1*4)当前的状态 ==> (1*4)4个action每个action的reward
            actions_value = self.sess.run(self.q_eval, feed_dict={self.s: observation})
            action = np.argmax(actions_value)#找最大reward的action
        else:
            #随机选择一个action
            action = np.random.randint(0, self.n_actions)
        return action

    def learn(self):
        #学习200次替换一次参数,target_net替换成eval_net
        if self.learn_step_counter % self.replace_target_iter == 0:
            self.sess.run(self.target_replace_op)
            print('\ntarget_params_replaced\n')

        #看memory中保存的数据来挑选32笔record的索引
        if self.memory_counter > self.memory_size:
            sample_index = np.random.choice(self.memory_size, size=self.batch_size)
        else:
            sample_index = np.random.choice(self.memory_counter, size=self.batch_size)
        batch_memory = self.memory[sample_index, :]#get record=>(32*10)

        _, cost = self.sess.run(
            [self._train_op, self.loss],
            feed_dict={self.s: batch_memory[:, :self.n_features],#32笔记录中的0-3列(32,[0-3])
                       self.a: batch_memory[:, self.n_features],#(32,[4])
                       self.r: batch_memory[:, self.n_features + 1],#(32,[5])
                       self.s_: batch_memory[:, -self.n_features:]})#(32,[6-9])

        self.cost_his.append(cost)#记录loss

        #该表e_greedy
        self.epsilon = self.epsilon + self.epsilon_increment if self.epsilon < self.epsilon_max else self.epsilon_max
        self.learn_step_counter += 1

    def plot_cost(self):
        import matplotlib.pyplot as plt
        plt.plot(np.arange(len(self.cost_his)), self.cost_his)
        plt.ylabel('Cost')
        plt.xlabel('training steps')
        plt.show()

class DeepQNetwork_01(DeepQNetwork):
    def __init__(self, n_actions, n_features, learning_rate=0.01, reward_decay=0.9, e_greedy=0.9,#4,4
                 replace_target_iter=300,#200
                 memory_size=500, batch_size=32,#2000,32
                 e_greedy_increment=None,
                 output_graph=False):
        super(DeepQNetwork, self).__init__(n_actions, n_features, learning_rate, reward_decay, e_greedy,
             replace_target_iter, memory_size, batch_size, e_greedy_increment, output_graph)
        
        t_params = tf.get_collection('target_net_params')
        e_params = tf.get_collection('eval_net_params')
        self.replace_target_op = [tf.assign(t, e) for t, e in zip(t_params, e_params)]
        
    def _build_net(self):
        self.s = tf.placeholder(tf.float32, [None, self.n_features], name='s')
        self.q_target = tf.placeholder(tf.float32, [None, self.n_actions], name='Q_target')
        with tf.variable_scope('eval_net'):#根据s算各个action的reward=>self.q_eval
            c_names, n_l1, w_initializer, b_initializer = ['eval_net_params', tf.GraphKeys.GLOBAL_VARIABLES], 10, tf.random_normal_initializer(0., 0.3), tf.constant_initializer(0.1)
            with tf.variable_scope('l1'):
                w1 = tf.get_variable('w1', [self.n_features, n_l1], initializer=w_initializer, collections=c_names)#创建在eval_net_params中的名字叫w1的Variable
                b1 = tf.get_variable('b1', [1, n_l1], initializer=b_initializer, collections=c_names)#创建在eval_net_params中的名字叫b1的Variable
                l1 = tf.nn.relu(tf.matmul(self.s, w1) + b1)#一个全连接,input是self.s
            with tf.variable_scope('l2'):
                w2 = tf.get_variable('w2', [n_l1, self.n_actions], initializer=w_initializer, collections=c_names)
                b2 = tf.get_variable('b2', [1, self.n_actions], initializer=b_initializer, collections=c_names)
                self.q_eval = tf.matmul(l1, w2) + b2
        
        with tf.variable_scope('loss'):
            self.loss = tf.reduce_mean(tf.squared_difference(self.q_target, self.q_eval))
        with tf.variable_scope('train'):
            self._train_op = tf.train.RMSPropOptimizer(self.lr).minimize(self.loss)
        
        self.s_ = tf.placeholder(tf.float32, [None, self.n_features], name='s_')
        with tf.variable_scope('target_net'):#根据s_算各个action的reward=>self.q_next
            c_names = ['target_net_params', tf.GraphKeys.GLOBAL_VARIABLES]#创建名字为target_net_params的collection
            with tf.variable_scope('l1'):
                w1 = tf.get_variable('w1', [self.n_features, n_l1], initializer=w_initializer, collections=c_names)
                b1 = tf.get_variable('b1', [1, n_l1], initializer=b_initializer, collections=c_names)
                l1 = tf.nn.relu(tf.matmul(self.s_, w1) + b1)#一个全连接层,输入是self.s_
            with tf.variable_scope('l2'):
                w2 = tf.get_variable('w2', [n_l1, self.n_actions], initializer=w_initializer, collections=c_names)
                b2 = tf.get_variable('b2', [1, self.n_actions], initializer=b_initializer, collections=c_names)
                self.q_next = tf.matmul(l1, w2) + b2
            
    def learn(self):
        if self.learn_step_counter % self.replace_target_iter == 0:
            self.sess.run(self.replace_target_op)
            print('\ntarget_params_replaced\n')
        if self.memory_counter > self.memory_size:
            sample_index = np.random.choice(self.memory_size, size=self.batch_size)
        else:
            sample_index = np.random.choice(self.memory_counter, size=self.batch_size)
        batch_memory = self.memory[sample_index, :]
        
        q_next, q_eval = self.sess.run(#算q_next和q_eval,计算出s时各个action的reward和s_时各个action的reward
            [self.q_next, self.q_eval],
            feed_dict={self.s_: batch_memory[:, -self.n_features:],
                       self.s: batch_memory[:, :self.n_features]})
        q_target = q_eval.copy()
        
        batch_index = np.arange(self.batch_size, dtype=np.int32)
        eval_act_index = batch_memory[:, self.n_features].astype(int)#action
        reward = batch_memory[:, self.n_features + 1]#reward
        
        #按照Q-learning计算reward,用于训练
        #batch = 2,n_actions = 4 ==> q_next = [[1, 2, 3, 4],[5, 6, 7, 8]], q_next=[[-1, -2, -3, -4],[-2, -3, -4, -5]], eval_act_index=[0, 2]
        #q_target = [[r[0]+g*-1, 2, 3, 4],[5, 6, r[1]+g*-2, 8]]
        q_target[batch_index, eval_act_index] = reward + self.gamma * np.max(q_next, axis=1)#计算q_target
        
        _, self.cost = self.sess.run([self._train_op, self.loss],
                                     feed_dict={self.s: batch_memory[:, :self.n_features], self.q_target: q_target})
        
        self.cost_his.append(self.cost)
        
        self.epsilon = self.epsilon + self.epsilon_increment if self.epsilon < self.epsilon_max else self.epsilon_max
        self.learn_step_counter += 1

def run_maze():
    step = 0
    for episode in range(args.get_option('dqn_06', 'MAX_EPISODES', 'int')):#最多完成300次(300个大回合)
        observation = env.reset()#初始化环境
        while True:
            env.render()#刷新环境
            action = brain.choose_action(observation)#根据当前state选择一个action,使用的实时学习网络给出的action
            observation_, reward, done = env.step(action)#选择这个action之后新的state,以及获得的奖励,以及是否完成这个回合
            brain.store_transition(observation, action, reward, observation_)#存储
            if (step > 200) and (step % 5 == 0):#memory中至少200条记录才可以开始学习,然后可以学习之后每5步就学习一次
                brain.learn()
            observation = observation_#更新state
            if done:#如果完成就开始下一大的回合
                break
            step += 1

    env.destroy()#环境销毁

if __name__ == "__main__":
    env = Maze()
    brain = DeepQNetwork(env.n_actions, env.n_features,#4,4
                         learning_rate=0.01, reward_decay=0.9, e_greedy=0.9,
                         replace_target_iter=200,#每200步替换一次target_net的参数
                         #output_graph=True,#是否输出tensorboard文件
                         memory_size=2000)#记忆SIZE
                     
    env.after(100, run_maze)
    env.mainloop()
    brain.plot_cost()#神经网络的误差曲线

#学习
#record = (s, a, r, s_)
#s -> eval_net -> 各个action的reward
#s_ -> target_net(eval_net的历史版本) -> 各个action的reward
#最小化2个算出的平方差

#获取下一步动作
#当前observation -> eval_net -> action(max)

#存储下所有的过程反复学习是一种off-policy的方法,可以自己玩,然后这个DQN会记录下来你是如何done的