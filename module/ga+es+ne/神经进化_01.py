# -*- coding: utf-8 -*-
'''
Created on Tue Mar  5 14:10:06 2019

@author: natasha_yang

@e-mail: ityangna0402@163.com
'''

#NEAT算法:安装install neat-python,可视化:graphviz(windows是exec文件[https://graphviz.gitlab.io/_pages/Download/Download_windows.html])
# 使用Innovation ID对神经网络direct coding
# 根据Innovation ID进行crossover
# 对神经元(node),神经链接(link)进行mutation
# 尽量保留生物多样性(Speciation)=>有些不好的网络说不定突然变异成超厉害的
# 通过初始化只有input连着output的神经网络来尽量减小神经网络的大小(从最小的神经网络结构开始发展)
#OpenAI提出的能够替代强化学习的ES
# 固定神经网络结构
# 使用正态分布来扰动(perturb)神经网络链接参数
# 使用扰动的网络在环境中收集奖励
# 用奖励(reward)或者效用(utility)来诱导参数更新幅度
#https://neat-python.readthedocs.io/en/latest/neat_overview.html
#有效的储存编码的神经网络
#有效的解码并生成一个可以正向传播的神经网络
#可视化网络结构
#NEAT的Recurrent link/node

#https://neat-python.readthedocs.io/en/latest/module_summaries.html#config
#实现异或操作

import os
import neat
import visualize as vs

xor_inputs = [(0.0, 0.0), (0.0, 1.0), (1.0, 0.0), (1.0, 1.0)]
xor_outputs = [(0.0,), (1.0,), (1.0,), (0.0,)]

def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = 4.0#初始分数
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        for xi, xo in zip(xor_inputs, xor_outputs):
            output = net.activate(xi)
            genome.fitness -= (output[0] - xo[0])**2#错误一次减一分

def run(config_file):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                         neat.DefaultStagnation, config_file)
    pop = neat.Population(config)
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    #每5次迭代生成一个checkpoint
    pop.add_reporter(neat.Checkpointer(50))
    winner = pop.run(eval_genomes, 300)
    
    print('Best genome:{!s}'.format(winner))
    
    print('Output:')
    
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
    for xi, xo in zip(xor_inputs, xor_outputs):
        output = winner_net.activate(xi)
        print('input {!r}, expected output {!r}, got {!r}'.format(xi, xo, output))
    node_names = {-1:'A', -2:'B', 0:'A XOR B'}
    #visulize
    #绘制net
    vs.draw_net(config, winner, True, node_names=node_names)
    #绘制最优和平均适应度,ylog表示y轴使用symlog(symmetric log)刻度
    vs.plot_stats(stats, ylog=False, view=True)
    #可视化种群变化
    vs.plot_species(stats, view=True)
    
    #使用restore_checkpoint方法使得种群pop恢复到的checkpoint-4时的状态,返回population
    pop = neat.Checkpointer.restore_checkpoint('neat-checkpoint-4')
    pop.run(eval_genomes, 10)

if __name__ == '__main__':
    os.environ['PATH'] += os.pathsep + 'D:/progress/graphviz/bin'#将graphviz加到路径中
    #construct配置文件路径
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, '神经进化_01.cfg')
    
    run(config_path)