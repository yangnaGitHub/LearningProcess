# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 11:18:18 2018

@author: Administrator
"""

import tensorflow as tf

one = tf.constant(1)
value = tf.Variable(0, name='value')

new_value = tf.add(one, value)
add_value = one + value

update = tf.assign(value, new_value)

init = tf.global_variables_initializer()

with tf.Session() as sess:
    sess.run(init)
    print(sess.run(new_value))
    print(sess.run(add_value))
    
    for _ in range(3):
        sess.run(update)
    print(sess.run(value))

#1
#1
#3