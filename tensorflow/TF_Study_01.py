# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 18:08:05 2018

@author: Administrator
"""

import tensorflow as tf

matrix_1 = tf.placeholder(tf.int32, [1, 3], name='matirx_1')
matrix_2 = tf.placeholder(tf.int32, [3, 1], name='matirx_2')
mulsum = tf.matmul(matrix_1, matrix_2)

sess = tf.Session()
mulsum_r = sess.run(mulsum, feed_dict={matrix_1:[[1, 2, 3]], matrix_2:[[3], [2], [1]]})
print(mulsum_r)