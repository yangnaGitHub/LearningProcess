# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 15:29:36 2016

@author: natasha1_Yang
"""

import numpy as np
from nn.data_utils import load_CIFAR10
import matplotlib.pyplot as plt
from basic.classifiers.linear_svm import svm_loss_naive
import time
from basic.gradient_check import grad_check_sparse
from basic.classifiers.linear_svm import svm_loss_vectorized
from basic.classifiers import LinearSVM
# 初始化的工作
#%matplotlib inline
plt.rcParams['figure.figsize'] = (10.0, 8.0) # set default size of plots
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'

# Some more magic so that the notebook will reload external python modules;
# see http://stackoverflow.com/questions/1907993/autoreload-of-modules-in-ipython
#%load_ext autoreload
#%autoreload 2

# 加载原始的CIFAR-10图片数据集
cifar10_dir = 'basic/datasets/cifar-10-batches-py'
X_train, y_train, X_test, y_test = load_CIFAR10(cifar10_dir)

# 看一眼训练集和测试集维度
print 'Training data shape: ', X_train.shape
print 'Training labels shape: ', y_train.shape
print 'Test data shape: ', X_test.shape
print 'Test labels shape: ', y_test.shape

# 可视化一下图片集，每个类别展示一些图片
classes = ['plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
num_classes = len(classes)
samples_per_class = 7
for y, cls in enumerate(classes):
    idxs = np.flatnonzero(y_train == y)
    idxs = np.random.choice(idxs, samples_per_class, replace=False)
    for i, idx in enumerate(idxs):
        plt_idx = i * num_classes + y + 1
        plt.subplot(samples_per_class, num_classes, plt_idx)
        plt.imshow(X_train[idx].astype('uint8'))
        plt.axis('off')
        if i == 0:
            plt.title(cls)
plt.show()

# 抽取训练集/交叉验证集/测试集
num_training = 49000
num_validation = 1000
num_test = 1000

# 取图
mask = range(num_training, num_training + num_validation)
X_val = X_train[mask]
y_val = y_train[mask]

mask = range(num_training)
X_train = X_train[mask]
y_train = y_train[mask]


mask = range(num_test)
X_test = X_test[mask]
y_test = y_test[mask]

print 'Train data shape: ', X_train.shape
print 'Train labels shape: ', y_train.shape
print 'Validation data shape: ', X_val.shape
print 'Validation labels shape: ', y_val.shape
print 'Test data shape: ', X_test.shape
print 'Test labels shape: ', y_test.shape

# 预处理：把数据展成一列
X_train = np.reshape(X_train, (X_train.shape[0], -1))
X_val = np.reshape(X_val, (X_val.shape[0], -1))
X_test = np.reshape(X_test, (X_test.shape[0], -1))

# 看一眼训练集和测试集维度
print 'Training data shape: ', X_train.shape
print 'Validation data shape: ', X_val.shape
print 'Test data shape: ', X_test.shape

# 预处理：减去图像均值
# 先求出训练集的均值
mean_image = np.mean(X_train, axis=0)
print mean_image[:10] # 输出一些均值数据看看
plt.figure(figsize=(4,4))
plt.imshow(mean_image.reshape((32,32,3)).astype('uint8')) # 可视化一下

# 然后从训练集和测试集里面减去图像均值
X_train -= mean_image
X_val -= mean_image
X_test -= mean_image

# 咱们把bias那一列1都加上
X_train = np.hstack([X_train, np.ones((X_train.shape[0], 1))]).T
X_val = np.hstack([X_val, np.ones((X_val.shape[0], 1))]).T
X_test = np.hstack([X_test, np.ones((X_test.shape[0], 1))]).T
# 看一眼维度
print X_train.shape, X_val.shape, X_test.shape

# 评估一下用for循环完成的svm_loss_naive的效果和效率:
# 产出SVM的初始权重
W = np.random.randn(10, 3073) * 0.0001 
loss, grad = svm_loss_naive(W, X_train, y_train, 0.00001)
print '损失值loss: %f' % (loss, )

# 咱们完成一下梯度的求解
# 然后做一下梯度检查

# 计算W下的梯度和损失.
loss, grad = svm_loss_naive(W, X_train, y_train, 0.0)

# 梯度检查，要检查数值梯度和解析梯度是否一致，因为解析梯度计算快，但是容易出错
f = lambda w: svm_loss_naive(w, X_train, y_train, 0.0)[0]
grad_numerical = grad_check_sparse(f, W, grad, 10)

# 然后咱们实现了一个非向量化的svm损失计算
tic = time.time()
loss_naive, grad_naive = svm_loss_naive(W, X_train, y_train, 0.00001)
toc = time.time()
print '非向量化的实现: 损失结果 %e 花费时间 %fs' % (loss_naive, toc - tic)

# 然后看看向量化的实现
tic = time.time()
loss_vectorized, _ = svm_loss_vectorized(W, X_train, y_train, 0.00001)
toc = time.time()
print '向量化的实现: 损失结果 %e 花费时间 %fs' % (loss_vectorized, toc - tic)

# 一般来说，如果你实现得正确，两个损失计算的结果是一致的，但是向量化的计算方法会快很多
print '两种方法差别: %f' % (loss_naive - loss_vectorized)
loss_vectorized, _ = svm_loss_vectorized(W, X_train, y_train, 0.00001)

# 咱们再比对一下2边的梯度是否一致
tic = time.time()
_, grad_naive = svm_loss_naive(W, X_train, y_train, 0.00001)
toc = time.time()
print '非向量化的实现计算损失和梯度花费时间 %fs' % (toc - tic)

tic = time.time()
_, grad_vectorized = svm_loss_vectorized(W, X_train, y_train, 0.00001)
toc = time.time()
print '向量化的实现计算损失和梯度花费时间 %fs' % (toc - tic)

# loss是一个值，直接比较就可以，但是梯度是一个矩阵，因此我们得用矩阵/向量的距离
difference = np.linalg.norm(grad_naive - grad_vectorized)
print '两种方法差别: %f' % difference

svm = LinearSVM()
tic = time.time()
loss_hist = svm.train(X_train, y_train, learning_rate=1e-7, reg=5e4,
                      num_iters=1500, verbose=True)
toc = time.time()
print '总共训练花费时间 %fs' % (toc - tic)

# 我们画出来随着迭代次数增多，损失的变化状况
plt.plot(loss_hist)
plt.xlabel('iteration number')
plt.ylabel('loss')

# 对样本进行预测并计算准确度
y_train_pred = svm.predict(X_train)
print '训练准确率: %f' % (np.mean(y_train == y_train_pred), )
y_val_pred = svm.predict(X_val)
print '验证集上准确率: %f' % (np.mean(y_val == y_val_pred), )

# 我们用交叉验证的方式测试不同的学习率
learning_rates = [5e-7, 1e-7, 5e-6, 1e-6, 1e-5]
regularization_strengths = [5e4, 1e5]

results = {}
best_val = -1   # 设定交叉验证最佳得分的初始值
best_svm = None # 设定交叉验证最佳svm参数集的初始值

verbose = True
for lr in learning_rates:
    for reg in regularization_strengths:
        if verbose: print "Training with hyper parameter learning rate: %e, regularization: %e " % ( lr, reg )
        svm = LinearSVM()
        loss_hist = svm.train(X_train, y_train, learning_rate=lr, reg=reg,
                      num_iters=1500, verbose=False)
        
        y_train_pred = svm.predict(X_train)
        training_accuracy = np.mean(y_train == y_train_pred)
        
        y_val_pred = svm.predict(X_val)
        val_accuracy = np.mean(y_val == y_val_pred)
        
        results[lr, reg] = (training_accuracy, val_accuracy)
        if val_accuracy > best_val:
            best_val = val_accuracy
            best_svm = svm
            
# 输出结果
for lr, reg in sorted(results):
    train_accuracy, val_accuracy = results[(lr, reg)]
    print '学习率 %e 正则化系数 %e 训练准确率: %f val accuracy: %f' % (
                lr, reg, train_accuracy, val_accuracy)
    
print '在交叉验证集上最好的准确率为: %f' % best_val

# 可视化交叉验证的结果
import math
x_scatter = [math.log10(x[0]) for x in results]
y_scatter = [math.log10(x[1]) for x in results]

# 画出训练准确率
sz = [results[x][0]*1500 for x in results] # default size of markers is 20
plt.subplot(1,2,1)
plt.scatter(x_scatter, y_scatter, sz)
plt.xlabel('log learning rate')
plt.ylabel('log regularization strength')
plt.title('CIFAR-10 training accuracy')

# 画出交叉验证集上的准确率
sz = [results[x][1]*1500 for x in results] # default size of markers is 20
plt.subplot(1,2,2)
plt.scatter(x_scatter, y_scatter, sz)
plt.xlabel('log learning rate')
plt.ylabel('log regularization strength')
plt.title('CIFAR-10 validation accuracy')

# 在测试集上看效果
y_test_pred = best_svm.predict(X_test)
test_accuracy = np.mean(y_test == y_test_pred)
print '在图像原始像素数据上训练的linear SVM分类器在实际测试集上的准确率为: %f' % test_accuracy

# 可视化每个类对应的权重
# 需要多说一句的是，因为初始值和学习率等的不同，你看到的结果可能会有一些差别
w = best_svm.W[:,:-1] # 去掉bias项
w = w.reshape(10, 32, 32, 3)
w_min, w_max = np.min(w), np.max(w)
classes = ['plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
for i in xrange(10):
  plt.subplot(2, 5, i + 1)
    
  # Rescale the weights to be between 0 and 255
  wimg = 255.0 * (w[i].squeeze() - w_min) / (w_max - w_min)
  plt.imshow(wimg.astype('uint8'))
  plt.axis('off')
  plt.title(classes[i])