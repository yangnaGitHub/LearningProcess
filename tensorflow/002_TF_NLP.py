# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 11:10:26 2018

@author: natasha1_Yang
"""

import random
import numpy as np

dataset = type('usage', (), {})()
def dummySampleTokenIdx():
    return random.randint(0, 4)

def getRandomContext(C):
    tokens = ['a', 'b', 'c', 'd', 'e']
    return tokens[random.randint(0, 4)], [tokens[random.randint(0, 4)] for i in xrange(2*C)]

dataset.sampleTokenIdx = dummySampleTokenIdx
dataset.getRandomContext = getRandomContext

def softmaxCostAndGradient(predicted, target, outputVectors):
    target_exp = np.exp(np.dot(np.reshape(predicted, (1, predicted.shape[0])), np.reshape(outputVectors[target], (outputVectors[target].shape[0], 1))))
    all_exp = np.exp(np.dot(outputVectors, np.reshape(predicted, (predicted.shape[0], 1))))
    all_sum_exp = np.sum(all_exp)
    prob = target_exp / all_sum_exp
    cost = -np.log(prob)
    gradTarget = -predicted + prob * predicted
    other_exp = np.vstack([all_exp[0:target], all_exp[target + 1:len(all_exp)]]).flatten()
    other_sigmoid = other_exp / all_sum_exp
    grad = np.dot(np.reshape(other_sigmoid, (other_sigmoid.shape[0], 1)), np.reshape(predicted, (1, predicted.shape[0])))
    grad = np.vstack([grad[0:target, :], gradTarget, grad[target:grad.shape[0], :]])
    repmat_exp = np.tile(all_exp, (1, outputVectors.shape[1]))
    gradPred = -outputVectors[target] + np.sum(outputVectors * repmat_exp, 0) / all_sum_exp
    return cost, gradPred, grad
    
def negSamplingCostAndGradient(predicted, target, outputVectors, K=10):
    neg_indexes = [dataset.sampleTokenIdx() for k in range(K)]
    r_W = np.dot(predicted, outputVectors.T)
    sigmoid_all = sigmoid(r_W)
    cost = -np.log(sigmoid_all[target]) - np.sum(np.log(1 - sigmoid_all[neg_indexes]))
    gradPred = -outputVectors[target, :] * (1 - sigmoid_all[target])
    gradPred += np.dot(sigmoid_all[neg_indexes], outputVectors[neg_indexes, :])
    grad = np.zeros(np.shape(outputVectors))
    grad[target, :] = -predicted * (1 - sigmoid_all[target])
    for neg_index in neg_indexes:
        grad[neg_index,:] += predicted * sigmoid_all[neg_index]
        ### END YOUR CODE 
    return cost, gradPred, grad

def skipgram(currentWord, C, contextWords, tokens, inputVectors, outputVectors, word2vecCostAndGradient = softmaxCostAndGradient):
    cost = 0
    predicted = inputVectors[tokens[currentWord]]
    gradIn = np.zeros(inputVectors.shape)
    gradOut = np.zeros(outputVectors.shape)
    for contextWord in contextWords:
        target = tokens[contextWord]
        contextCost, contextGradPred, contextGrad = word2vecCostAndGradient(predicted, target, outputVectors)
        cost += contextCost
        gradIn[tokens[currentWord],:] += contextGradPred
        gradOut += contextGrad
        ### END YOUR CODE 
    return cost, gradIn, gradOut

def cbow(currentWord, C, contextWords, tokens, inputVectors, outputVectors, word2vecCostAndGradient = softmaxCostAndGradient):
    in_rows = inputVectors.shape[0]
    in_cols = inputVectors.shape[1]  
    all_context_indx = np.zeros(2 * C)
    for c in range(2 * C + 1):
        if c == C:
            target = tokens[currentWord]
        elif c < C:
            all_context_indx[c] = tokens[contextWords[c]]
        else:
            all_context_indx[c - 1] = tokens[contextWords[c - 1]]   
    gradIn = np.zeros((in_rows, in_cols))   
    all_context_indx_list = list(np.array(all_context_indx, int))
    h = np.mean(inputVectors[all_context_indx_list], 0)
    cost, gradInTem, gradOut = word2vecCostAndGradient(h, target, outputVectors)
    for context_indx in all_context_indx:
        gradIn[context_indx] += gradInTem
    gradIn = gradIn / 2 / C    
    return cost, gradIn, gradOut
    
https://www.cnblogs.com/baiboy/p/learnnlp.html#top

https://blog.csdn.net/u011534057/article/details/53067110 tensorflow
https://blog.csdn.net/u011534057/article/category/6507827 tensorflow
https://www.cnblogs.com/skyfsm/p/6806246.html RCNN
http://karpathy.github.io/2015/05/21/rnn-effectiveness/ RCNN
https://zhuanlan.zhihu.com/p/25167153 yolo2


有些问题得到了基本解决，如：词性标注、命名实体识别、垃圾邮件识别。
有些问题取得长足进展，如：情感分析、共指消解、词义消歧、句法分析、机器翻译、信息抽取。
有些问题依然充满挑战，如：自动问答、复述、文摘提取、会话机器人等。

分词
编辑距离MED:指两个字符串之间，由一个转成另一个所需要的最少编辑操作次数(提供用于拼写纠错的侯选单词)
朴素贝叶斯分类器 垃圾邮件
失去了词语之间的顺序信息==>词袋子模型(bag of words)

推荐系统：是的，你没听错，是用在推荐系统里！！朴素贝叶斯和协同过滤(Collaborative Filtering)是一对好搭档，协同过滤是强相关性，但是泛化能力略弱，朴素贝叶斯和协同过滤一起，能增强推荐的覆盖度和效果。

