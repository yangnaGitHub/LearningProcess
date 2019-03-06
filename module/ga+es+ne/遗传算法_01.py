# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 18:15:44 2019

@author: natasha_yang

@e-mail: ityangna0402@163.com
"""

#在程序中生宝宝,杀死不乖的宝宝,让乖宝宝继续生宝宝
import numpy as np
import matplotlib.pyplot as plt

DNA_SIZE = 10#DNA的长度
POP_SIZE = 100#人口的多少
CROSS_RATE = 0.8
MUTATION_RATE = 0.003
N_GENERATIONS = 200
X_BOUND = [0, 5]
def F(x_val): return np.sin(10*x_val)*x_val + np.cos(2*x_val)*x_val
#找一个评估好坏的方程=>fitness
def get_fitness(pred):
    return pred + 1e-3 - np.min(pred)
#转换成DNA,二进制装换成十进制,就是用0-1023的二进制转换成0-5的十进制
def translateDNA(pop):#POP_SIZE, DNA_SIZE
    #[0, 1, 2, 3, 4, 5, 6, 7, 8, 9] => [  1,   2,   4,   8,  16,  32,  64, 128, 256, 512] => [512, 256, 128,  64,  32,  16,   8,   4,   2,   1]
    #np.dot是点积x1*y1+x2*y2+x3*y3 => (POP_SIZE, DNA_SIZE)*(1*10)=>1*POP_SIZE
    return pop.dot(2 ** np.arange(DNA_SIZE)[::-1]) / float(2 ** DNA_SIZE-1) * X_BOUND[1]
#进化:DNA交叉配对 + DNA变异 + 适者生存
#适者生存
def select(pop, fitness):
    idx = np.random.choice(np.arange(POP_SIZE), size=POP_SIZE, replace=True, p=fitness/fitness.sum())
    return pop[idx]#这是在排优先级???
#父母的基因交叉配对
def crossover(parent, pop):
    #parent:[0, 0, 1, 0, 1, 1, 1, 0, 0, 0]   =>      0       0 0
    #pop[i_]:[0, 1, 0, 0, 1, 1, 1, 0, 1, 0]  =>0 1 0   1 1 1     0
    #cross_points:[ True,  True,  True, False,  True,  True,  True, False, False, True]
    #[0, 1, 0, 0, 1, 1, 1, 0, 0, 0]
    if np.random.rand() < CROSS_RATE:
        i_ = np.random.randint(0, POP_SIZE, size=1)#0-POP_SIZE选择一个数,随便选择一个父母
        cross_points = np.random.randint(0, 2, size=DNA_SIZE).astype(np.bool)
        parent[cross_points] = pop[i_, cross_points]
    return parent
#基因变异
def mutate(child):
    for point in range(DNA_SIZE):
        if np.random.rand() < MUTATION_RATE:
            child[point] = 1 if child[point] == 0 else 0
    return child

plt.ion()
x_val = np.linspace(*X_BOUND, 200)#0,5分成200个数据
plt.plot(x_val, F(x_val))

#种群DNA
pop = np.random.randint(2, size=(POP_SIZE, DNA_SIZE))#由0,1(randint)构成的POP_SIZE*DNA_SIZE的数组
for _ in range(N_GENERATIONS):
    trans_pop = translateDNA(pop)#将种群的DNA转换成十进制的0-5之间的数值
    F_values = F(trans_pop)
    
    if 'sca' in globals():#globals返回全局变量的字典
        sca.remove()
    sca = plt.scatter(trans_pop, F_values, s=200, lw=0, c='red', alpha=0.5)
    plt.pause(0.05)
    
    fitness = get_fitness(F_values)
    print('most fitted DAN: ', pop[np.argmax(fitness), :])
    pop = select(pop, fitness)#按照适应度选择应该留下来的pop
    pop_copy = pop.copy()
    for parent in pop:
        child = crossover(parent, pop_copy)#DNA交叉配对
        child = mutate(child)#DNA交叉配对
        parent[:] = child#孩子长大替换父母
plt.ioff()
plt.show()

#我的问题:
#1.人口集合一直没有变化,孩子只有一个替换自己的父亲
#2.适者生存我没有看出是怎么表达的,只是修改了先后顺序