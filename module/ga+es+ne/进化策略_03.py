# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 11:25:36 2019

@author: natasha_yang

@e-mail: ityangna0402@163.com
"""

#http://www.jmlr.org/papers/volume15/wierstra14a/wierstra14a.pdf
#NES:用适应度诱导的梯度下降,生宝宝,用乖宝宝的梯度辅助找到前进的方向
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.contrib.distributions import MultivariateNormalFullCovariance#多元正态分布
#协方差:衡量两个变量的总体误差
#cov(X, Y) = E{[X - E(X)][Y - E(Y)]}

DNA_SIZE = 2
N_POP = 20
N_GENERATION = 100
LR = 0.02

def get_fitness(pred): return -((pred[:, 0]**2) + (pred[:, 1]**2))

#shape, mean, stddev
mean = tf.Variable(tf.random_normal([2,], 13., 1.), dtype=tf.float32)
cov = tf.Variable(5.*tf.eye(DNA_SIZE), dtype=tf.float32)#tf.eye单位矩阵(2*2)
mvn = MultivariateNormalFullCovariance(loc=mean, covariance_matrix=cov)
make_kid = mvn.sample(N_POP)#sample生成指定形状的样本

tfkids_fit = tf.placeholder(tf.float32, [N_POP, ])#(20,)
tfkids = tf.placeholder(tf.float32, [N_POP, DNA_SIZE])#(20,2)
#梯度*fitness加大力度往带来好fitness的梯度下降
loss = -tf.reduce_mean(mvn.log_prob(tfkids)*tfkids_fit)#log_prob记录概率密度/质量函数
train_op = tf.train.GradientDescentOptimizer(LR).minimize(loss)

sess = tf.Session()
sess.run(tf.global_variables_initializer())

count = 300
x_val_l = np.linspace(-20, 20, count)
x_val,y_val = np.meshgrid(x_val_l, x_val_l)
z_val = np.zeros_like(x_val)#(300, 300)

for x_index in range(count):
    for y_index in range(count):
        try:
            z_val[x_index, y_index] = get_fitness(np.array([[x_val_l[x_index], x_val_l[y_index]]]))
        except ValueError:
            print('index:', x_index, y_index)
            print(len(x_val[x_index]), len(x_val[y_index]))
            
plt.contourf(x_val, y_val, -z_val, 100, cmap=plt.cm.rainbow)#填充等高线
plt.xlim(-20, 20)
plt.ylim(-20, 20)
plt.ion()

for _ in range(N_GENERATION):
    kids = sess.run(make_kid)
    #print(kids.shape)#20*2
    kids_fit = get_fitness(kids)
    sess.run(train_op, {tfkids_fit:kids_fit, tfkids:kids})
    if 'sca' in globals(): sca.remove()
    sca = plt.scatter(kids[:, 0], kids[:, 1], s=30, c='k')
    plt.pause(0.01)

plt.ioff()
plt.show()

#每一次训练是放入的kids_fit和kids,训练的目的是让loss变小
#那kids来自于make_kid=>mvn=>mean + cov(是训练的这个)