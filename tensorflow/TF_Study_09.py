# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 16:57:45 2018

@author: Administrator
"""

import tensorflow as tf
import numpy as np
import os
import struct
from tensorflow.contrib.tensorboard.plugins import projector

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

pic_num = 3000
embedding = tf.Variable(tf.stack(x_test[:pic_num]), trainable=False, name='embedding')

#参数概要
def variable_summary(var):
    mean = tf.reduce_mean(var)
    tf.summary.scalar('mean', mean)
    std = tf.sqrt(tf.reduce_mean(tf.square(var - mean)))
    tf.summary.scalar('stddev', std)
    tf.summary.scalar('max', tf.reduce_max(var))
    tf.summary.scalar('min', tf.reduce_min(var))
    tf.summary.histogram('histogram', var)

#构建模块开始,使用name_scope为一个单元的
with tf.name_scope('input'):
    x = tf.placeholder(tf.float32, [None, 784], name='x_input')
    y = tf.placeholder(tf.float32, [None, 10], name='y_input')

with tf.name_scope('layers'):
    with tf.name_scope('weights'):
        w = tf.Variable(tf.truncated_normal([784, 10], stddev=0.1), name='w')
        variable_summary(w)
    with tf.name_scope('bias'):
        b = tf.Variable(tf.zeros([10]) + 0.1, name='b')
        variable_summary(b)
    with tf.name_scope('outputs'):
        o = tf.matmul(x, w) + b
    with tf.name_scope('realoutputs'):
        ro = tf.nn.softmax(o)

with tf.name_scope('loss'):
    loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(labels=y, logits=ro))
    tf.summary.scalar('loss', loss)

with tf.name_scope('train'):
    train = tf.train.GradientDescentOptimizer(0.2).minimize(loss)

with tf.name_scope('accuracy'):
    with tf.name_scope('result'):
        result = tf.equal(tf.argmax(y, 1), tf.argmax(ro, 1))
    with tf.name_scope('accuracy'):
        accuracy = tf.reduce_mean(tf.cast(result, tf.float32))
#构建模块结束
        
#显示图片
with tf.name_scope('input_reshape'):
    image_shaped_input = tf.reshape(x, [-1, 28, 28, 1])
    tf.summary.image('input', image_shaped_input, 10)#取10张图片

COMMON_PATH = 'E:/AboutStudy/code/python/'
projector_path = COMMON_PATH + 'projector/projector'
metadata_path = COMMON_PATH + 'projector/projector/metadata.tsv'
image_path = COMMON_PATH + 'projector/data/mnist_10k_sprite.png'
model_path = COMMON_PATH + 'projector/projector/a_model.ckpt'

init = tf.global_variables_initializer()
merge = tf.summary.merge_all()

sess = tf.Session()

with tf.Session() as sess:
    sess.run(init)
    saver = tf.train.Saver()
    
    if tf.gfile.Exists(metadata_path):
        tf.gfile.DeleteRecursively(projector_path)
    if not tf.gfile.Exists(projector_path):
        tf.gfile.MakeDirs(projector_path)
    with open(metadata_path, mode='w') as fd:
        labels = sess.run(tf.argmax(y_test, 1))
        for index in range(pic_num):
            fd.write(str(labels[index]) + '\n')
    projector_writer = tf.summary.FileWriter(projector_path, sess.graph)
    config = projector.ProjectorConfig()
    embed = config.embeddings.add()
    embed.tensor_name = embedding.name
    embed.metadata_path = metadata_path
    embed.sprite.image_path = image_path
    embed.sprite.single_image_dim.extend([28, 28])
    projector.visualize_embeddings(projector_writer, config)
    
    max_steps = 1000
    for index in range(max_steps):
        run_options = tf.RunOptions(trace_level=tf.RunOptions.FULL_TRACE)
        run_metadata = tf.RunMetadata()
        startindex = index * 100
        summary, _ = sess.run([merge, train], feed_dict={x:x_train[startindex:startindex+100], y:y_train[startindex:startindex+100]}, options=run_options, run_metadata=run_metadata)
        projector_writer.add_run_metadata(run_metadata, 'step%03d' % index)
        projector_writer.add_summary(summary, index)
        
    saver.save(sess, model_path, global_step=max_steps)
    projector_writer.close()

#运行方式cmd ==> tensorboard.exe --logdir=E:\AboutStudy\code\python\projector\projector
 #最后打印TensorBoard 1.7.0 at http://WINDOWS-6NOBA61:6006 (Press CTRL+C to quit)
 #浏览器访问提示的http://WINDOWS-6NOBA61:6006即可