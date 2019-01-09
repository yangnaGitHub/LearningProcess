# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 17:46:07 2018

@author: Administrator
"""

import tensorflow as tf
import numpy as np

#准备数据
np.random.seed(0)
x_data = np.random.rand(100).astype(np.float32)
y_data = 0.3*x_data + 0.1

#初始化参数
weight = tf.Variable(tf.random_uniform([1], -1.0, 1.0))
bias = tf.Variable(tf.zeros([1]))


y = weight * x_data + bias
#构建loss
loss = tf.reduce_mean(tf.square(y - y_data))
#使用啥学习,梯度下降
#optimizer = tf.train.GradientDescentOptimizer(0.5)
optimizer = tf.train.AdamOptimizer(0.5)#自适应的方法学习
#目的是啥
train = optimizer.minimize(loss)

#开始做任务
init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)
for step in range(501):
    sess.run(train)
    if step % 20 == 0:
        print("step: ", step, sess.run(weight), sess.run(bias))

#流程
 #准备数据
 #初始化参数
 #构建模型
  #loss函数定义
  #学习方法
  #优化目的是啥