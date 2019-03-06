# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 18:24:48 2019

@author: natasha_yang

@e-mail: ityangna0402@163.com
"""

import neat
import numpy as np
import gym
import visualize as vs
import os

env = gym.make('CartPole-v0').unwrapped
EP_STEP = 300
GENERATION_EP = 10
TRAINING = False#True进化,False输出最优网络
CHECKPOINT = 9#最终状态

def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        ep_r = []
        for ep in range(GENERATION_EP):#最多10个大循环
            accumulative_r = 0.
            observation = env.reset()#每次循环环境重置
            for step in range(EP_STEP):#每次大循环保证坐300次小循环直至成功
                action_values = net.activate(observation)#从当前状态计算各个action的值
                action = np.argmax(action_values)#选择最大的
                observation_, reward, done, _ = env.step(action)#执行这个action后得到的状态和奖励以及是否完成
                accumulative_r += reward#奖励
                if done:
                    break
                observation = observation_#更新当前的状态
            ep_r.append(accumulative_r)
        genome.fitness = np.min(ep_r)/float(EP_STEP)#算成是最终的fitness

def run(config_file):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)
    pop = neat.Population(config)
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    pop.add_reporter(neat.StdOutReporter(True))
    pop.add_reporter(neat.Checkpointer(5))#neat-checkpoint-4,neat-checkpoint-9
    
    pop.run(eval_genomes, 10)
    
    vs.plot_stats(stats, ylog=False, view=True)
    vs.plot_species(stats, view=True)

def evaluation():
    pop = neat.Checkpointer.restore_checkpoint('neat-checkpoint-%i' % CHECKPOINT)
    winner = pop.run(eval_genomes, 1)
    node_names = {-1: 'In0', -2: 'In1', -3: 'In3', -4: 'In4', 0: 'act1', 1: 'act2'}
    vs.draw_net(pop.config, winner, True, node_names=node_names)
    net = neat.nn.FeedForwardNetwork.create(winner, pop.config)
    while True:
        state = env.reset()
        while True:
            env.render()
            action = np.argmax(net.activate(state))
            state, reward, done, _ = env.step(action)
            if done:
                break
    
if __name__ == '__main__':
    os.environ['PATH'] += os.pathsep + 'D:/progress/graphviz/bin'#将graphviz加到路径中
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, '神经进化_02.cfg')
    if TRAINING:
        run(config_path)
    else:
        evaluation()
#HyperNEAT
#ES-HyperNEAT