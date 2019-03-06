# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 13:56:20 2019

@author: natasha_yang

@e-mail: ityangna0402@163.com
"""

#如何有效保留好的父母:Microbial GA(MGA)
import numpy as np
import matplotlib.pyplot as plt

DNA_SIZE = 10
POP_SIZE = 20
CROSS_RATE = 0.6
MUTATION_RATE = 0.01
N_GENERATIONS = 200
X_BOUND = [0, 5]

def F(x_val): return np.sin(10*x_val)*x_val + np.cos(2*x_val)*x_val

class MGA(object):
    def __init__(self, DNA_size, DNA_bound, cross_rate, mutation_rate, pop_size):
        self.DNA_size = DNA_size
        DNA_bound[1] += 1
        self.DNA_bound = DNA_bound
        self.cross_rate = cross_rate
        self.mutate_rate = mutation_rate
        self.pop_size = pop_size
        self.pop = np.random.randint(*DNA_bound, size=(1, self.DNA_size)).repeat(pop_size, axis=0)#20*10,每一行的值是一样的
    
    def translateDNA(self, pop):
        #np.dot是点积x1*y1+x2*y2+x3*y3
        return pop.dot(2**np.arange(self.DNA_size)[::-1]) / float(2**self.DNA_size - 1) * X_BOUND[1]
    
    def get_fitness(self, pred):
        return pred
    
    def crossover(self, loser_winner):
        cross_idx = np.empty((self.DNA_size,)).astype(np.bool)
        for index in range(self.DNA_size):
            cross_idx[index] = True if np.random.rand() < self.cross_rate else False
        loser_winner[0, cross_idx] = loser_winner[1, cross_idx]#loser中替换成winner中的基因
        return loser_winner
    
    def mutate(self, loser_winner):
        mutation_idx = np.empty((self.DNA_size,)).astype(np.bool)
        for index in range(self.DNA_size):
            mutation_idx[index] = True if np.random.rand() < self.mutate_rate else False
        #记住这个写法,可以在指定(mutation_idx为True的地方)的地方翻转
        loser_winner[0, mutation_idx] = ~loser_winner[0, mutation_idx].astype(np.bool)
        return loser_winner
    
    def evolve(self, count):
        #选择count对
        for index in range(count):
            sub_pop_idx = np.random.choice(np.arange(0, self.pop_size), size=2, replace=False)#在0~self.pop_size之间选择2个,replace=False抽样之后还放不放回去
            sub_pop = self.pop[sub_pop_idx]#随机选择的2个DNA
            product = F(self.translateDNA(sub_pop))#对这两个DNA求转换值
            fitness = self.get_fitness(product)#求fitness
            loser_winner_idx = np.argsort(fitness)#排序,按照从小到大
            loser_winner = sub_pop[loser_winner_idx]#排序后的DNA
            loser_winner = self.crossover(loser_winner)
            loser_winner = self.mutate(loser_winner)
            self.pop[sub_pop_idx] = loser_winner
        DNA_prod = self.translateDNA(self.pop)
        pred = F(DNA_prod)
        return DNA_prod, pred

plt.ion()
x_val = np.linspace(*X_BOUND, 200)
plt.plot(x_val, F(x_val))

mga = MGA(DNA_size=DNA_SIZE, DNA_bound=[0, 1], cross_rate=CROSS_RATE, mutation_rate=MUTATION_RATE, pop_size=POP_SIZE)
for _ in range(N_GENERATIONS):
    DNA_prod, pred = mga.evolve(5)
    if 'sca' in globals(): sca.remove()
    sca = plt.scatter(DNA_prod, pred, s=200, lw=0, c='red', alpha=0.5)
    plt.pause(0.05)

plt.ioff()
plt.show()