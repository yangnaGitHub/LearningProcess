# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 14:03:31 2018

@author: Administrator
"""

import tensorflow as tf
import numpy as np
import os
import struct

#利用TF下载
#from tensorflow.examples.tutorials.mnist import input_data
#minist = input_data.read_data_sets('E:\AboutStudy\code\python\MNIST_data', one_hot=True)

#整数据
MNIST_PATH = 'E:\AboutStudy\code\python\mnist'
def load_mnist(path, kind='train'):
    labels_path = os.path.join(path, '%s-labels.idx1-ubyte' % kind)
    images_path = os.path.join(path, '%s-images.idx3-ubyte' % kind)
    with open(labels_path, mode='rb') as lfd:
        magic, n = struct.unpack('>II', lfd.read(8))
        labels = np.fromfile(lfd, dtype=np.uint8)
    with open(images_path, mode='rb') as ifd:
        magic, num, rows, cols = struct.unpack('>IIII', ifd.read(16))
        images = np.fromfile(ifd, dtype=np.uint8).reshape(len(labels), 784)
    r_labels = np.zeros([labels.shape[0], 10])#label的onehot编码,验证精确集的时候是取的下标,分到的是哪一类
    for index, value in enumerate(labels):
        r_labels[index][value] = 1
    return images, r_labels
x_train, y_train = load_mnist(MNIST_PATH)
x_test, y_test = load_mnist(MNIST_PATH, kind='t10k')

#输入
x = tf.placeholder(tf.float32, [None, 784])
y = tf.placeholder(tf.float32, [None, 10])

#构建模型
w1 = tf.Variable(tf.zeros([784, 10]))#输入是784 输出是10
b1 = tf.Variable(tf.zeros([10]))
o1 = tf.matmul(x, w1) + b1
ro1 = tf.nn.softmax(o1)

#判断好坏,定义损失函数
loss = tf.reduce_mean(tf.square(ro1 - y))
#loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(labels=y, logits=ro1))

#怎么学习
optimizer = tf.train.GradientDescentOptimizer(0.2)
#optimizer = tf.train.AdamOptimizer(1e-2)
#目标是啥
train = optimizer.minimize(loss)

#如何检验
#有2种操作,第一种就是直接定义在TF图中,另外一种就是使用PYTHON的手法(得到预测值直接算精确率)
result = tf.equal(tf.argmax(ro1, 1), tf.argmax(y, 1))#1代表以列来取最大值下标
accuracy = tf.reduce_mean(tf.cast(result, tf.float32))#cast转类型(bool转float)

#存在Variable,所以要初始化
init = tf.global_variables_initializer()
with tf.Session() as sess:
    sess.run(init)
    #开始训练
     #数据过大,分成一个一个包来训练,要分成多少个包,每个包有batch_num大
    batch_num = 100
    each_batch = x_train.shape[0] // batch_num
    for epoch in range(201):#跑多少圈
        #batch 训练
        for batchindex in range(each_batch):
            startindex = batchindex * batch_num
            sess.run(train, feed_dict={x:x_train[startindex:startindex+batch_num], y:y_train[startindex:startindex+batch_num]})
        #20步检测一下精确率
        if epoch % 20 == 0:
            acc = sess.run(accuracy, feed_dict={x:x_test, y:y_test})
            print("Iter:"+str(epoch)+", accuracy:"+str(acc))
    #训练完成预测 ==> 如何检验(2)
    #predict = sess.run(ro1, feed_dict={x:x_test})
    #计算精确率
    #predict != y_test

#优化环节
 #1>损失函数
  #使用的是传统的MSE的损失函数,可以使用交叉熵等其他损失函数
  #loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(labels=y, logits=ro1))
 #2>怎么学习(优化方式),使用自适应的学习方式,会计算一阶导数和二阶导数
 #optimizer = tf.train.AdamOptimizer(1e-2)#1e-2代表10的负二次方
 #3>单层网络变换成多层网络
  #多层网络可能导致过拟合dropout,(层数多了也不行)
 #4>调参数,比如学习率等动态调整