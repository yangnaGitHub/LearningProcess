# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 13:56:44 2019

@author: natasha_yang

@e-mail: ityangna0402@163.com
"""

import numpy as np

TARGET_PHRASE = 'you get it'
POP_SIZE = 300
CROSS_RATE = 0.4
MUTATION_RATE = 0.01
N_GENERATIONS = 1000
DNA_SIZE = len(TARGET_PHRASE)
TARGET_ASCII = np.fromstring(TARGET_PHRASE, dtype=np.uint8)#将字符串转化成ASCII码
#TARGET_ASCII = np.frombuffer(TARGET_PHRASE, dtype=np.uint8)#将字符串转化成ASCII码
ASCII_BOUND = [32, 127]

class GA_PHASE(object):
    def __init__(self, DNA_size, DNA_bound, cross_rate, mutation_rate, pop_size):
        self.DNA_size = DNA_size
        self.DNA_bound = DNA_bound
        self.cross_rate = cross_rate
        self.mutate_rate = mutation_rate
        self.pop_size = pop_size
        self.pop = np.random.randint(*DNA_bound, size=(pop_size, DNA_size)).astype(np.int8)#300*10
    
    def translateDNA(self, DNA):
        return DNA.tostring().decode('ascii')#将[32,127]之间的数值转化成ascii码
    
    def get_fitness(self):#要提供目标
        match_count = (self.pop == TARGET_ASCII).sum(axis=1)#匹配度
        return match_count
    
    def select(self):
        fitness = self.get_fitness() + 1e-4
        idx = np.random.choice(np.arange(self.pop_size), size=self.pop_size, replace=True, p=fitness/fitness.sum())
        return self.pop[idx]
    
    def crossover(self, parent, pop):
        if np.random.rand() < self.cross_rate:
            i_ = np.random.randint(0, self.pop_size, size=1)
            cross_points = np.random.randint(0, 2, self.DNA_size).astype(np.bool)
            parent[cross_points] = pop[i_, cross_points]
        return parent
    
    def mutate(self, child):
        for point in range(self.DNA_size):
            if np.random.rand() < self.mutate_rate:
                child[point] = np.random.randint(*self.DNA_bound)#编译变成32-127中的其中一个数值,变异可不可以变异成重来没有出现过的呢
        return child

    def evolve(self):
        pop = self.select()
        pop_copy = pop.copy()
        for parent in pop:
            child = self.crossover(parent, pop_copy)
            child = self.mutate(child)
            parent[:] = child
        self.pop = pop

if __name__ == '__main__':
    ga_phase = GA_PHASE(DNA_size=DNA_SIZE, DNA_bound=ASCII_BOUND, cross_rate=CROSS_RATE, mutation_rate=MUTATION_RATE, pop_size=POP_SIZE)
    for generation in range(N_GENERATIONS):
        fitness = ga_phase.get_fitness()
        best_DNA = ga_phase.pop[np.argmax(fitness)]
        best_phase = ga_phase.translateDNA(best_DNA)
        print('Gen', generation, ': ', best_phase)
        if TARGET_PHRASE == best_phase:
            break
        ga_phase.evolve()