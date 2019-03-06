# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 15:11:17 2019

@author: natasha_yang

@e-mail: ityangna0402@163.com
"""

#遗传算法和进化算法的区别
#遗传:选择好父母之后进行繁殖,进化:先繁殖,然后选择好的孩子
#遗传:二进制编码,要转化,进化:DNA是实数
#遗传:随机让翻转变异,进化:通过正态分布变异
#进化的DNA形式2条DNA,一个DNA是控制数值,第二个DNA是控制这个数值的变异强度
#比如DNA1=1.23, -0.13, 2.35, 112.5可以理解为4个正态分布的4个平均值
#    DNA2=0.1, 2.44, 5.112, 2.144可以理解为4个正态分布的4个标准差,两条DNA都需要被crossover和mutate

import numpy as np
import matplotlib.pyplot as plt

DNA_SIZE = 1
DNA_BOUND = [0, 5]
N_GENERATIONS = 200
POP_SIZE = 100
N_KID = 50

def F(x_val): return np.sin(10*x_val)*x_val + np.cos(2*x_val)*x_val

def get_fiteness(pred):
    return pred.flatten()

#根据正态分布生孩子
def make_kid(pop, n_kid):
    kids = {'DNA': np.empty((n_kid, DNA_SIZE))}#50*1
    kids['mut_strength'] = np.empty_like(kids['DNA'])#50*1
    for kv,ks in zip(kids['DNA'], kids['mut_strength']):
        #crossover
        cp1, cp2 = np.random.choice(np.arange(POP_SIZE), size=2, replace=False)#在100个随便选中2个
        cp = np.random.randint(0, 2, DNA_SIZE, dtype=np.bool)#true和false中选择DNA_SIZE
        #cp决定选择来自cp1还是cp2,cp=True选择pop[cp1],cp=False选择pop[cp2]
        kv[cp] = pop['DNA'][cp1, cp]
        kv[~cp] = pop['DNA'][cp2, ~cp]
        ks[cp] = pop['mut_strength'][cp1, cp]
        ks[~cp] = pop['mut_strength'][cp2, ~cp]
        
        #mutate
        ks[:] = np.maximum(ks + (np.random.rand(*ks.shape) - 0.5), 0.)#返回*ks.shape服从0~1均匀分布的随机样本
        kv += ks*np.random.randn(*kv.shape)
        #np.clip截取的意思,超出的部分就把它强置为边界部分
        kv[:] = np.clip(kv, *DNA_BOUND)
    return kids

#杀了哪些坏孩子和坏父母
def kill_bad(pop, kids):
    for key in ['DNA', 'mut_strength']:
        pop[key] = np.vstack((pop[key], kids[key]))#100 + 50 = 150,孩子和父母中选择
    fitness = get_fiteness(F(pop['DNA']))
    idx = np.arange(pop['DNA'].shape[0])
    good_idx = idx[fitness.argsort()][-POP_SIZE:]#选择fitness好的100个,淘汰50个
    for key in ['DNA', 'mut_strength']:
        pop[key] = pop[key][good_idx]
    return pop

plt.ion()
x_val = np.linspace(*DNA_BOUND, 200)
plt.plot(x_val, F(x_val))

pop = dict(DNA=5*np.random.rand(1, DNA_SIZE).repeat(POP_SIZE, axis=0),#均值,POP_SIZE*DNA_SIZE(100*1)
           mut_strength=np.random.rand(POP_SIZE, DNA_SIZE))#标准差
for _ in range(N_GENERATIONS):
    if 'sca' in globals(): sca.remove()
    sca = plt.scatter(pop['DNA'], F(pop['DNA']), s=200, lw=0, c='red', alpha=0.5)
    plt.pause(0.05)
    
    kids = make_kid(pop, N_KID)
    pop = kill_bad(pop, kids)
plt.ioff()
plt.show()