# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 11:31:27 2018

@author: Administrator
"""

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

#x_data = np.linspace(-0.5, 0.5, 200)#shape = (200,)
#构造数据
x_data = np.linspace(-0.5,0.5,200)[:, np.newaxis]#shape = (200, 1) np.newaxis新起一个维度
noise = np.random.normal(0, 0.02, x_data.shape)
y_data = np.square(x_data) + noise

#构造输入
x = tf.placeholder(tf.float32, [None, 1])#x_data
y = tf.placeholder(tf.float32, [None, 1])#y_data
#设计好结构 ==> 2层的感知神经深度学习网络
 #需要2层参数w1 w2 b1 b2
 #确定每一层的神经元的个数 第一层10个,后面一层1个(所以w1[1, 10], w2[10, 1](输入是第一层的10个))
 #每一层的输出o1 o2以及是否经过激励层ro1 ro2
w1 = tf.Variable(tf.random_normal([1, 10]))
b1 = tf.Variable(tf.zeros([1, 10]))
o1 = tf.matmul(x, w1) + b1
ro1 = tf.nn.tanh(o1)

w2 = tf.Variable(tf.random_normal([10, 1]))
b2 = tf.Variable(tf.zeros([1, 1]))
o2 = tf.matmul(ro1, w2) + b2
ro2 = tf.nn.tanh(o2)#最终输出的值

#定义损失函数
loss = tf.reduce_mean(tf.square(ro2 - y))
#使用啥优化
#optimizer = tf.train.AdamOptimizer(0.2)#学习率
optimizer = tf.train.GradientDescentOptimizer(0.2)#学习率,这个优化要快一些
#要达到什么目的
train = optimizer.minimize(loss)

#网络搭建完成,开始训练过程
 #存在tf.Variable所以要统一初始化参数
init = tf.global_variables_initializer()
with tf.Session() as sess:
    sess.run(init)
    #多轮训练
    for _ in range(2001):
        sess.run(train, feed_dict={x:x_data, y:y_data})
        #分类问题可以在训练问题过程中打印精确率
    #训练过程完成
    predict_value = sess.run(ro2, feed_dict={x:x_data})
    plt.figure()
    plt.scatter(x_data, y_data)
    plt.plot(x_data, predict_value, 'b-', lw=5)
    plt.show()



