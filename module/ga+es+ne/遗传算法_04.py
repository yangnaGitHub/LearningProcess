# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 10:17:18 2019

@author: natasha_yang

@e-mail: ityangna0402@163.com
"""

import matplotlib.pyplot as plt
import numpy as np

N_MOVES = 150
DNA_SIZE = N_MOVES*2
DIRECTION_BOUND = [0, 2]
CROSS_RATE = 0.8
MUTATE_RATE = 0.0001
POP_SIZE = 100
N_GENERATIONS = 100
GOAL_POINT = [10, 5]
START_POINT = [0, 5]
OBSTACLE_LINE = np.array([[5, 2], [5, 8]])

class GA_PATH(object):
    def __init__(self, DNA_size, DNA_bound, cross_rate, mutation_rate, pop_size):
        self.DNA_size = DNA_size#N_MOVES*2=>300
        self.DNA_bound = DNA_bound#[0,2]
        self.cross_rate = cross_rate
        self.mutate_rate = mutation_rate
        self.pop_size = pop_size#100
        #*DNA_bound=>0, 1
        self.pop = np.random.randint(*DNA_bound, size=(pop_size, DNA_size))#100*300,左开右闭0和1构成
    
    #每一个DNA前面是x的变化量,后面是y的变化量,每一个数据代表向前面走多少,所以累加
    #最后一个数据应该是最后的坐标x,y=>lines_x[:, -1], lines_y[:, -1]
    def DNA2product(self, DNA, n_moves, start_point):#100*300
        pop = (DNA - 0.5) / 2#0=>-0.25, 1=>0.25
        pop[:, 0], pop[:, n_moves] = start_point[0], start_point[1]#第1列替换成0, 第151列替换成5,共300列,每列100个数据
        #返回给定axis上的累计和
        #arr = [1,2,3,4,5,6,7]
        #np.cumsum(arr) => [  1,   3,   6,  10,  15,  21,  28,  36,  45,  55,  75, 105]
        #axis=0:行累加,axis=1:列累加
        #arr=[[1,2,3],[4,5,6],[7,8,9]] => np.cumsum(arr,axis=1)
        #[[ 1,  3,  6],
        # [ 4,  9, 15],
        # [ 7, 15, 24]]
        lines_x = np.cumsum(pop[:, :n_moves], axis=1)#前150列累加和=>100*150
        lines_y = np.cumsum(pop[:, n_moves:], axis=1)#后150列累加和=>100*150
        return lines_x, lines_y
    
    def get_fitness(self, lines_x, lines_y, goal_point, obstacle_line):
        #所有DNA(线)求距离
        dist2goal = np.sqrt((goal_point[0] - lines_x[:, -1]) ** 2 + (goal_point[1] - lines_y[:, -1]) ** 2)#求预测点和目标点的欧式距离
        fitness = np.power(1 / (dist2goal + 1), 2)#+1的目的是防止为0,由求最小转化为求最大
        
        points = (lines_x > obstacle_line[0, 0] - 0.5) & (lines_x < obstacle_line[1, 0] + 0.5)#lines_x是否属于(4.5, 5.5)之间
        #np.where(condition, x, y),满足条件,输出x,否则输出y
        y_values = np.where(points, lines_y, np.zeros_like(lines_y) - 100)#x不在(4.5, 5.5)之间的y的值都是-100
        bad_lines = ((y_values > obstacle_line[0, 1]) & (y_values < obstacle_line[1, 1])).max(axis=1)#每一行有没有经过障碍的,只要返回true就一定是经过
        fitness[bad_lines] = 1e-6#经过障碍的fitness的值很小
        return fitness
    
    def select(self, fitness):
        idx = np.random.choice(np.arange(self.pop_size), size=self.pop_size, replace=True, p=fitness/fitness.sum())#根据fitness的大小选择
        return self.pop[idx]
    
    def crossover(self, parent, pop):
        if np.random.rand() < self.cross_rate:
            i_ = np.random.randint(0, self.pop_size, size=1)
            cross_points = np.random.randint(0, 2, self.DNA_size).astype(np.bool)
            parent[cross_points] = pop[i_, cross_points]
        return parent
    
    def mutate(self, child):
        for point in range(self.DNA_size):
            if np.random.rand() < self.mutate_rate:#0-1均匀分布
                child[point] = np.random.randint(*self.DNA_bound)
        return child
    
    def evolve(self, fitness):
        pop = self.select(fitness)
        pop_copy = pop.copy()
        for parent in pop:
            child = self.crossover(parent, pop_copy)
            child = self.mutate(child)
            parent[:] = child
        self.pop = pop

class Line(object):
    #问题描述:寻找从[0.5]开始到[10,5]结束的直线要避过[5,2]到[5, 8]的直线
    def __init__(self, n_moves, goal_point, start_point, obstacle_line):
        self.n_moves = n_moves#150
        self.goal_point = goal_point#[10, 5]
        self.start_point = start_point#[0, 5]
        self.obstacle_line = obstacle_line#[5, 2], [5, 8]
        plt.ion()
        
    def plotting(self, lines_x, lines_y):
        plt.cla()
        plt.scatter(*self.goal_point, s=200, c='r')#目标点
        plt.scatter(*self.start_point, s=100, c='b')#起始点
        plt.plot(self.obstacle_line[:, 0], self.obstacle_line[:, 1], lw=3, c='k')
        plt.plot(lines_x.T, lines_y.T, c='k')
        plt.xlim((-5, 15))
        plt.ylim((-5, 15))
        plt.pause(0.01)

ga_path = GA_PATH(DNA_size=DNA_SIZE, DNA_bound=DIRECTION_BOUND, cross_rate=CROSS_RATE, mutation_rate=MUTATE_RATE, pop_size=POP_SIZE)
env = Line(N_MOVES, GOAL_POINT, START_POINT, OBSTACLE_LINE)

for generation in range(N_GENERATIONS):
    lx, ly = ga_path.DNA2product(ga_path.pop, N_MOVES, START_POINT)
    fitness = ga_path.get_fitness(lx, ly, GOAL_POINT, OBSTACLE_LINE)
    ga_path.evolve(fitness)
    print('Gen: ', generation, '| best fit:', fitness.max())
    env.plotting(lx, ly)

plt.ioff()
plt.show()