# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 14:47:10 2018

@author: natasha1_Yang
"""

import numpy as np
import tensorflow as tf
import tensorflow.contrib.rnn as rnn
import tensorflow.contrib.crf as crf
import time

LEARNING_RATE=0.001                 #学习率
MAX_SENTENCE_SIZE=32                #固定句子长度为32
TIMESTEP_SIZE=MAX_SENTENCE_SIZE     #LSTM的time_step应该和句子长度一致
INPUT_SIZE=EMBEDDING_SIZE=64        #嵌入向量维度,和输入大小应当一样
DECAY=0.85
MAX_EPOCH=5                         #最大迭代次数
LAYER_NUM=2                         #lstm层数2
HIDDEN_UNITS_NUM=128                #隐藏层结点数量
HIDDEN_UNITS_NUM2=128               #隐藏层2结点数量
CLASS_NUM=5                         #类别数量
VOCAB_SIZE=5159                     # 样本中不同字的个数+1(padding 0)，根据处理数据的时候得到
BATCH_SIZE=1024                     #batch大小
DROPOUT_RATE=0.5                    #dropout 比率

class BiLSTM:
    def __init__(self):
        self.graph = tf.Graph()
        self.session = tf.Session(graph=self.graph)
        
        #parameter
        self.learning_rate = LEARNING_RATE
        self.max_epoch = MAX_EPOCH
        self.embedding_size = EMBEDDING_SIZE
        self.class_num = CLASS_NUM
        self.hidden_units_num = HIDDEN_UNITS_NUM
        self.layer_num = LAYER_NUM
        self.max_sentence_size = MAX_SENTENCE_SIZE
        self.vocab_size = VOCAB_SIZE
        self.batch_size = BATCH_SIZE
    
    def fit(self, X_train, y_train, X_validation, y_validation, name, print_log=True):
        with self.graph.as_default():
            self.X_p = tf.placeholder(dtype=tf.int32, shape=(None, self.max_sentence_size), name='input_placeholder')
            self.y_p = tf.placeholder(dtype=tf.int32, shape=(None, self.max_sentence_size), name='label_placeholder')
            embeddings = tf.Variable(initial_value=tf.zeros(shape=(self.vocab_size, self.embedding_size), dtype=tf.float32), name='embeddings')
            inputs = tf.nn.embedding_lookup(params=embeddings, ids=self.X_p, name='embeded_input')
            
            #forward part
            lstm_forward1 = rnn.BasicLSTMCell(num_units=self.hidden_units_num)
            lstm_forward2 = rnn.BasicLSTMCell(num_units=self.class_num)
            lstm_forward = rnn.MultiRNNCell(cells=[lstm_forward1, lstm_forward2])
            
            #backward part
            lstm_backward1 = rnn.BasicLSTMCell(num_units=self.hidden_units_num)
            lstm_backward2 = rnn.BasicLSTMCell(num_units=self.class_num)
            lstm_backward = rnn.MulitRNNCell(cells=[lstm_backward1, lstm_backward2])
            
            outputs, states = tf.nn.bidirectional_rnn(cell_fw=lstm_forward, cell_bw=lstm_backward, inputs=inputs, dtype=tf.float32)
            outputs_forward = outputs[0]
            outputs_backward = outputs[1]
            pred = outputs_forward + outputs_backward
            print pred.shape
            
            pred_2 = tf.reshape(tensor=pred, shape=[-1, 5], name='pred')
            print pred_2.shape
            
            correct_prediction = tf.equal(tf.cast(tf.argmax(pred_2, 1), tf.int32), tf.reshape(self.y_p, [-1]))
            print correct_prediction.shape
            
            self.accuracy = tf.reduce_mean(input_tensor=tf.cast(x=correct_prediction, dtype=tf.float32), name='accuracy')
            self.loss = tf.losses.sparse_softmax_cross_entropy(labels=tf.reshape(self.y_p, shape=[-1]), logits=pred_2)
            self.optimizer = tf.train.AdamOptimizer(learning_rate=self.learning_rate).minimize(self.loss)
            self.init_op = tf.global_variables_initializer()
        
        with self.session as sess:
            sess.run(self.init_op)
            best_validation_accuracy = 0
            train_size = X_train.shape[0]
            validation_size = X_validation.shape[0]
            for epoch in range(1, self.max_epoch+1):
                start_time = time.time()
                train_losses = []
                train_accus = []
                for i in range(0, (train_size // self.batch_size)):
                    _, train_loss, train_accuracy = sess.run(fetches=[self.optimizer, self.loss, self.accuracy],
                                                             feed_dict={
                                                                        self.X_p:X_train[i*self.batch_size:(i+1)*self.batch_size],
                                                                        self.y_p:y_train[i*self.batch_size:(i+1)*self.batch_size]
                                                                        })
                    if print_log:
                        print 'Mini-Batch: ', i*self.batch_size, '~', (i+1)*self.batch_size, 'of epoch:', epoch
                        print '     training loss: ', train_loss
                        print '     training accuracy: ', train_accuracy
                        print
                    train_losses.append(train_loss)
                    train_accus.append(train_accuracy)
                
        