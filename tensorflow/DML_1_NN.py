# -*- coding: utf-8 -*-
"""
Created on Tue Nov 08 21:09:30 2016

@author: natasha1_Yang
"""

import numpy as np
import matplotlib.pyplot as plt
import os
from nn.classifiers.neural_net import two_layer_net
from nn.gradient_check import eval_numerical_gradient
from nn.classifier_trainer import ClassifierTrainer
from nn.data_utils import load_CIFAR10
from nn.classifiers.neural_net import init_two_layer_model
from nn.vis_utils import visualize_grid

#%matplotlib inline
plt.rcParams['figure.figsize'] = (10.0, 8.0) # set default size of plots
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'

# for auto-reloading external modules
# see http://stackoverflow.com/questions/1907993/autoreload-of-modules-in-ipython
#%load_ext autoreload
#%autoreload 2

def rel_error(x, y):
    """ 返回相对误差 """
    return np.max(np.abs(x - y) / (np.maximum(1e-8, np.abs(x) + np.abs(y))))
  
# 随机初始化一个试验模型(其实就是存在dic中的权重)和数据集
input_size = 4
hidden_size = 10
num_classes = 3
num_inputs = 5

def init_toy_model():
    model = {}
    model['W1'] = np.linspace(-0.2, 0.6, num=input_size*hidden_size).reshape(input_size, hidden_size)
    model['b1'] = np.linspace(-0.3, 0.7, num=hidden_size)
    model['W2'] = np.linspace(-0.4, 0.1, num=hidden_size*num_classes).reshape(hidden_size, num_classes)
    model['b2'] = np.linspace(-0.5, 0.9, num=num_classes)
    return model

def init_toy_data():
    X = np.linspace(-0.2, 0.5, num=num_inputs*input_size).reshape(num_inputs, input_size)
    y = np.array([0, 1, 2, 2, 1])
    return X, y

model = init_toy_model()
X, y = init_toy_data()


scores = two_layer_net(X, model, verbose=True)
print scores
correct_scores = [[-0.5328368, 0.20031504, 0.93346689],
                  [-0.59412164, 0.15498488, 0.9040914 ],
                  [-0.67658362, 0.08978957, 0.85616275],
                  [-0.77092643, 0.01339997, 0.79772637],
                  [-0.89110401, -0.08754544, 0.71601312]]

# 我们前向运算计算得到的得分和实际的得分应该差别很小才对
print '前向运算得到的得分和实际的得分差别:'
print np.sum(np.abs(scores - correct_scores))

reg = 0.1
loss, _ = two_layer_net(X, model, y, reg)
correct_loss = 1.38191946092

# 应该差值是很小的
print '我们计算到的损失和真实的损失值之间差别:'
print np.sum(np.abs(loss - correct_loss))

# 使用数值梯度去检查反向传播的计算

loss, grads = two_layer_net(X, model, y, reg)

# 各参数应该比 1e-8 要小才保险
for param_name in grads:
    param_grad_num = eval_numerical_gradient(lambda W: two_layer_net(X, model, y, reg)[0], model[param_name], verbose=False)
    print '%s 最大相对误差: %e' % (param_name, rel_error(param_grad_num, grads[param_name]))
  


model = init_toy_model()
trainer = ClassifierTrainer()
# 这个地方是自己手造的数据，量不大，所以其实sample_batches就设为False了，直接全量梯度下降
best_model, loss_history, _, _ = trainer.train(X, y, X, y,
                                               model, two_layer_net,
                                               reg=0.001,
                                               learning_rate=1e-1, momentum=0.0, learning_rate_decay=1,
                                               update='sgd', sample_batches=False,
                                               num_epochs=100,
                                               verbose=False)
print 'Final loss with vanilla SGD: %f' % (loss_history[-1], )

model = init_toy_model()
trainer = ClassifierTrainer()
# call the trainer to optimize the loss
# Notice that we're using sample_batches=False, so we're performing Gradient Descent (no sampled batches of data)
best_model, loss_history, _, _ = trainer.train(X, y, X, y,
                                               model, two_layer_net,
                                               reg=0.001,
                                               learning_rate=1e-1, momentum=0.9, learning_rate_decay=1,
                                               update='momentum', sample_batches=False,
                                               num_epochs=100,
                                               verbose=False)
correct_loss = 0.494394
print 'Final loss with momentum SGD: %f. We get: %f' % (loss_history[-1], correct_loss)

model = init_toy_model()
trainer = ClassifierTrainer()
# call the trainer to optimize the loss
# Notice that we're using sample_batches=False, so we're performing Gradient Descent (no sampled batches of data)
best_model, loss_history, _, _ = trainer.train(X, y, X, y,
                                               model, two_layer_net,
                                               reg=0.001,
                                               learning_rate=1e-1, momentum=0.9, learning_rate_decay=1,
                                               update='rmsprop', sample_batches=False,
                                               num_epochs=100,
                                               verbose=False)
correct_loss = 0.439368
print 'Final loss with RMSProp: %f. We get: %f' % (loss_history[-1], correct_loss)

def get_CIFAR10_data(num_training=49000, num_validation=1000, num_test=1000):
    """
    载入CIFAR-10数据集，并做预处理。这一步和前一节课用softmax和SVM分类是一样的
    """
    cifar10_dir = 'nn/datasets/cifar-10-batches-py'
    X_train, y_train, X_test, y_test = load_CIFAR10(cifar10_dir)
        
    # 采样数据
    mask = range(num_training, num_training + num_validation)
    X_val = X_train[mask]
    y_val = y_train[mask]
    mask = range(num_training)
    X_train = X_train[mask]
    y_train = y_train[mask]
    mask = range(num_test)
    X_test = X_test[mask]
    y_test = y_test[mask]

    # 去均值
    mean_image = np.mean(X_train, axis=0)
    X_train -= mean_image
    X_val -= mean_image
    X_test -= mean_image

    # 调整维度
    X_train = X_train.reshape(num_training, -1)
    X_val = X_val.reshape(num_validation, -1)
    X_test = X_test.reshape(num_test, -1)

    return X_train, y_train, X_val, y_val, X_test, y_test


# 看看数据维度
X_train, y_train, X_val, y_val, X_test, y_test = get_CIFAR10_data()
print 'Train data shape: ', X_train.shape
print 'Train labels shape: ', y_train.shape
print 'Validation data shape: ', X_val.shape
print 'Validation labels shape: ', y_val.shape
print 'Test data shape: ', X_test.shape
print 'Test labels shape: ', y_test.shape

model = init_two_layer_model(32*32*3, 100, 10) # input size, hidden size, number of classes
trainer = ClassifierTrainer()
best_model, loss_history, train_acc, val_acc = trainer.train(X_train, y_train, X_val, y_val,
                                                             model, two_layer_net,
                                                             num_epochs=5, reg=1.0,
                                                             momentum=0.9, learning_rate_decay = 0.95,
                                                             learning_rate=1e-5, verbose=True)
#看到loss的下降近乎是线性的，这预示着可能我们的学习率设得太小了
#训练和交叉验证集上的准确率差别又不是特别大，也可能说明模型的容量（学习能力）很有限，可以提高隐层的结点个数
#训练集和交叉验证集上可能准确率差别就会很大了，这有可能说明是过拟合
plt.subplot(2, 1, 1)#2 * 1==>1
plt.plot(loss_history)
plt.title('Loss history')
plt.xlabel('Iteration')
plt.ylabel('Loss')

plt.subplot(2, 1, 2)
plt.plot(train_acc)
plt.plot(val_acc)
plt.legend(['Training accuracy', 'Validation accuracy'], loc='lower right')
plt.xlabel('Epoch')
plt.ylabel('Clasification accuracy')

# 可视化权重

def show_net_weights(model):
    plt.imshow(visualize_grid(model['W1'].T.reshape(-1, 32, 32, 3), padding=3).astype('uint8'))
    plt.gca().axis('off')
    plt.show()

show_net_weights(model)

#调优
best_model = None # 存储交叉验证集上拿到的最好的结果
best_val_acc = -1
# 很不好意思，这里直接列了一堆参数，然后用for循环做的cross-validation
learning_rates = [1e-5, 5e-5, 1e-4]
model_capacitys = [200, 300, 500, 1000]
regularization_strengths = [1e0, 1e1]
results = {}
verbose = True

for hidden_size in model_capacitys:
    for lr in learning_rates:
        for reg in regularization_strengths:
            if verbose: 
                print "Trainging Start: "
                print "lr = %e, reg = %e, hidden_size = %e" % (lr, reg, hidden_size)

            model = init_two_layer_model(32*32*3, hidden_size, 10)
            trainer = ClassifierTrainer()
            output_model, loss_history, train_acc, val_acc = trainer.train(X_train, y_train, X_val, y_val,
                                             model, two_layer_net,
                                             num_epochs=5, reg=1.0,
                                             momentum=0.9, learning_rate_decay = 0.95,
                                             learning_rate=lr)


            results[hidden_size, lr, reg] = (loss_history, train_acc, val_acc)

            if verbose: 
                print "Training Complete: "
                print "Training accuracy = %f, Validation accuracy = %f " % (train_acc[-1], val_acc[-1])

            if val_acc[-1] > best_val_acc:
                best_val_acc = val_acc[-1]
                best_model = output_model
        
print 'best validation accuracy achieved during cross-validation: %f' % best_val_acc

# 可视化参数权重
show_net_weights(best_model)

# 在测试集上看准确率
scores_test = two_layer_net(X_test, best_model)
print 'Test accuracy: ', np.mean(np.argmax(scores_test, axis=1) == y_test)

total_num = len(results)
for i, (hsize, lr, reg) in enumerate(sorted(results)):
    loss_history, train_acc, val_acc = results[hsize, lr, reg]
    
    if val_acc[-1] > 0.5: 
        plt.figure(i)
        plt.title('hidden size {0} lr {1} reg {2} train accuracy'.format(hsize, lr, reg))
        
        plt.subplot(2, 1, 1)
        plt.plot(loss_history)
        plt.title('Loss history')
        plt.xlabel('Iteration')
        plt.ylabel('Loss')

        plt.subplot(2, 1, 2)
        plt.plot(train_acc)
        plt.plot(val_acc)
        plt.legend(['Training accuracy', 'Validation accuracy'], loc='lower right')
        plt.xlabel('Epoch')
        plt.ylabel('Clasification accuracy')
        
scores_test = two_layer_net(X_test, best_model)
print 'Test accuracy: ', np.mean(np.argmax(scores_test, axis=1) == y_test)