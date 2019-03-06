# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 15:42:08 2019

@author: natasha_yang

@e-mail: ityangna0402@163.com
"""

import numpy as np
import matplotlib.pyplot as plt

N_CITIES = 20
CROSS_RATE = 0.1
MUTATE_RATE = 0.02
POP_SIZE = 500
N_GENERATIONS = 500

class GA_CITY(object):
    def __init__(self, DNA_size, cross_rate, mutation_rate, pop_size):
        self.DNA_size = DNA_size#20
        self.cross_rate = cross_rate
        self.mutate_rate = mutation_rate
        self.pop_size = pop_size#500
        #np.random.permutation随机排列一个序列,返回一个排列的序列
        self.pop = np.vstack([np.random.permutation(DNA_size) for _ in range(pop_size)])#初始化的DNA集群有500个随机生成的20个城市的排列序列
    
    #将每个DNA转化成城市位置的序列
    def translateDNA(self, DNA, city_position):#500*20, 20*2
        line_x = np.empty_like(DNA, dtype=np.float64)#500*20的随机矩阵
        line_y = np.empty_like(DNA, dtype=np.float64)#500*20的随机矩阵
        for index,DNA_data in enumerate(DNA):#DNA_data:1*20作为索引
            city_coord = city_position[DNA_data]#是将city_position按照DNA_data排了一个序=>20*2
            line_x[index, :] = city_coord[:, 0]#20*1第一列
            line_y[index, :] = city_coord[:, 1]#20*1第二列
        return line_x, line_y
    
    def get_fitness(self, line_x, line_y):
        total_distance = np.empty((line_x.shape[0],), dtype=np.float64)#np.empty()返回一个随机元素的矩阵,500
        for index,(xs,ys) in enumerate(zip(line_x, line_y)):#xs:1*20 ys:1*20
            #np.diff沿着指定轴计算第N维的离散差值 
            #x = np.array([1, 2, 4, 7, 0]) =>np.diff(x):[ 1,  2,  3, -7]
            #算每个DNA(城市序列)的距离
            total_distance[index] = np.sum(np.square(np.diff(xs)) + np.square(np.diff(ys)))#np.square计算数组各元素的平方
        fitness = np.exp(self.DNA_size*2 / total_distance)#e的幂次方
        return fitness, total_distance
    
    #问题不同,所以策略不同
    def select(self, fitness):
        idx = np.random.choice(np.arange(self.pop_size), size=self.pop_size, replace=True, p=fitness/fitness.sum())
        return self.pop[idx]
    
    def crossover(self, parent, pop):
        #每个城市都要出现一次,父亲的按照顺序先出现,母亲的在按照顺序出现
        if np.random.rand() < self.cross_rate:
            i_ = np.random.randint(0, self.pop_size, size=1)
            cross_points = np.random.randint(0, 2, self.DNA_size).astype(np.bool)
            #cross_points:[ True, False, False,  True, False,  True]
            #parent:[0, 1, 2, 3, 4, 5] => [1, 2, 4]
            keep_city = parent[~cross_points]
            #np.isin(1,2)判断1中的是否在2中出现
            #np.isin([0, 2], [1, 2]) => [False, True]
            #np.isin([0, 2], [1, 2], invert=True) => [True, False]
            #扁平化操作:flatten()分配了新的内存,ravel()是一个数组的视图
            #np.isin([5, 4, 3, 2, 1, 0], [1, 2, 4], invert=True) => [ True, False,  True, False, False,  True]
            swap_city = pop[i_, np.isin(pop[i_].ravel(), keep_city, invert=True)]
            parent[:] = np.concatenate((keep_city, swap_city))
        return parent

    def mutate(self, child):
        for point in range(self.DNA_size):
            if np.random.rand() < self.mutate_rate:
                swap_point = np.random.randint(0, self.DNA_size)
                swapA, swapB = child[point], child[swap_point]#城市之间两点交换
                child[point], child[swap_point] = swapB, swapA
        return child
    
    def evolve(self, fitness):
        pop = self.select(fitness)
        pop_copy = pop.copy()
        for parent in pop:
            child = self.crossover(parent, pop_copy)
            child = self.mutate(child)
            parent[:] = child
        self.pop = pop

class TravelSalesPerson(object):
    def __init__(self, n_cities):
        self.city_position = np.random.rand(n_cities, 2)#0-1均匀分布的随机样本值(20*2)=>当做20个城市的坐标
        plt.ion()#打开交互模式
    
    def plotting(self, lx, ly, total_d):
        plt.cla()
        plt.scatter(self.city_position[:, 0].T, self.city_position[:, 1].T, s=100, c='k')
        plt.plot(lx.T, ly.T, 'r-')
        plt.text(-0.05, -0.05, 'total distance=%.2f' % total_d, fontdict={'size':14, 'color':'red'})
        plt.xlim((-0.1, 1.1))
        plt.ylim((-0.1, 1.1))
        plt.pause(0.01)

ga_city = GA_CITY(DNA_size=N_CITIES, cross_rate=CROSS_RATE, mutation_rate=MUTATE_RATE, pop_size=POP_SIZE)
env = TravelSalesPerson(N_CITIES)
for generation in range(N_GENERATIONS):#500轮
    lx, ly = ga_city.translateDNA(ga_city.pop, env.city_position)
    fitness, total_distance = ga_city.get_fitness(lx, ly)
    ga_city.evolve(fitness)
    best_idx = np.argmax(fitness)
    print('Gen: ', generation, '| best fit: %.2f' % fitness[best_idx])
    env.plotting(lx[best_idx], ly[best_idx], total_distance[best_idx])

plt.ioff()#显示前关掉交互模式
plt.show()
#我在想这和全遍历计算的距离的差别在哪儿
#适者生存的优势体现在哪儿,有一个引导性的
#如果全遍历的话不会这么快,回合太多,遗传算法可以利用适者生存可以快速返回最优答案