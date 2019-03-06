# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 10:53:34 2019

@author: natasha_yang

@e-mail: ityangna0402@163.com
"""

#1+1-ES:一个爸爸和一个孩子的战争
#有多种形式
#1.有一个爸爸
#  根据爸爸变异出一个宝宝
#  在爸爸和宝宝中选好的那个变成下一代爸爸

import numpy as np
import matplotlib.pyplot as plt

DNA_SIZE = 1
DNA_BOUND = [0, 5]
N_GENERATIONS = 100
MUT_STRENGTH = 5.

def F(x_val): return np.sin(10*x_val)*x_val + np.cos(2*x_val)*x_val

def get_fitness(pred): return pred.flatten()

def make_kid(parent):
    kid = parent + MUT_STRENGTH*np.random.randn(DNA_SIZE)#MUT_STRENGTH*np.random.randn(DNA_SIZE)=>变异
    kid = np.clip(kid, *DNA_BOUND)
    return kid

def kill_bad(parent, kid):
    global MUT_STRENGTH
    fp = get_fitness(F(parent))[0]
    fk = get_fitness(F(kid))[0]
    p_target = 1/5#如果有1/5的变异比原始的parent好的话,就是快收敛了
    if fp < fk:
        parent = kid
        ps = 1.#MUT_STRENGTH变大
    else:
        ps = 0.#MUT_STRENGTH变小
    MUT_STRENGTH *= np.exp(1/np.sqrt(DNA_SIZE+1) * (ps-p_target)/(1-p_target))
    return parent

plt.ion()
x_val = np.linspace(*DNA_BOUND, 200)

parent = 5*np.random.rand(DNA_SIZE)
for _ in range(N_GENERATIONS):
    kid = make_kid(parent)
    py,ky = F(parent), F(kid)
    parent = kill_bad(parent, kid)
    
    plt.cla()
    plt.scatter(parent, py, s=200, lw=0, c='red', alpha=0.5)
    plt.scatter(kid, ky, s=200, lw=0, c='blue', alpha=0.5)
    plt.text(0, -7, 'Mutation strength=%.2f' % MUT_STRENGTH)
    plt.plot(x_val, F(x_val))
    plt.pause(0.05)
plt.ioff()
plt.show()