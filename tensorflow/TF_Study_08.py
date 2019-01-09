# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 15:57:49 2018

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

#构建模型 ==> 使用多层网络(使用3层网络)第一层500,第二层300,第三层输出10
l1 = 500
l2 = 300

w1 = tf.Variable(tf.truncated_normal([784, l1], stddev=0.1))#输入是784 输出是1000 初始化参数使用截断高斯
b1 = tf.Variable(tf.zeros([l1]) + 0.1)#默认值是0.1
o1 = tf.matmul(x, w1) + b1
ro1 = tf.nn.tanh(o1)

w2 = tf.Variable(tf.truncated_normal([l1, l2], stddev=0.1))#输入是1000 输出是1500 初始化参数使用截断高斯
b2 = tf.Variable(tf.zeros([l2]) + 0.1)#默认值是0.1
o2 = tf.matmul(ro1, w2) + b2
ro2 = tf.nn.tanh(o2)

w3 = tf.Variable(tf.truncated_normal([l2, 10], stddev=0.1))#输入是1500 输出是10 初始化参数使用截断高斯
b3 = tf.Variable(tf.zeros([10]) + 0.1)#默认值是0.1
o3 = tf.matmul(ro2, w3) + b3
ro3 = tf.nn.softmax(o3)#输出

#判断好坏,定义损失函数
#loss = tf.reduce_mean(tf.square(ro1 - y))
loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(labels=y, logits=ro3))

#怎么学习
lr = tf.Variable(0.001, dtype=tf.float32)#动态学习率
#optimizer = tf.train.GradientDescentOptimizer(0.2)
optimizer = tf.train.AdamOptimizer(lr)
#目标是啥
train = optimizer.minimize(loss)

#如何检验
result = tf.equal(tf.argmax(ro3, 1), tf.argmax(y, 1))#1代表以列来取最大值下标
accuracy = tf.reduce_mean(tf.cast(result, tf.float32))#cast转类型(bool转float)

#存在Variable,所以要初始化
init = tf.global_variables_initializer()
with tf.Session() as sess:
    sess.run(init)
    #开始训练
     #数据过大,分成一个一个包来训练,要分成多少个包,每个包有batch_num大
    batch_num = 100
    each_batch = x_train.shape[0] // batch_num
    for epoch in range(21):#跑多少圈
        #batch 训练
        sess.run(tf.assign(lr, 0.001*(0.95**epoch)))
        for batchindex in range(each_batch):
            startindex = batchindex * batch_num
            sess.run(train, feed_dict={x:x_train[startindex:startindex+batch_num], y:y_train[startindex:startindex+batch_num]})
        learning_rating = sess.run(lr)
        acc = sess.run(accuracy, feed_dict={x:x_test, y:y_test})
        print("Iter:"+str(epoch)+", learning rating:"+str(learning_rating)+", accuracy:"+str(acc))