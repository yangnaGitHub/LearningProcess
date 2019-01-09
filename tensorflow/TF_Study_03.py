# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 11:24:21 2018

@author: Administrator
"""

import tensorflow as tf

x_data = tf.constant(2.0)
y_data = tf.constant(3.0)

add_data = tf.add(x_data, y_data)
sub_data = tf.subtract(add_data, y_data)

with tf.Session() as sess:
    print(sess.run([add_data, sub_data]))

input1 = tf.placeholder(tf.float32)
input2 = tf.placeholder(tf.float32)

update = tf.multiply(input1, input2)
with tf.Session() as sess:
    print(sess.run(update, feed_dict={input1:2.0, input2:3.0}))

#使用tf.Variable的时候有用global_variables_initializer初始化变量