# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 13:42:21 2019

@author: yangna

@e-mail: ityangna0402@163.com
"""

#强化学习上的ES,在自己附近生宝宝,让自己更像那些表现好的宝宝
#不断地试错,然后每一次试错后,让自己更靠近到那些返回更多奖励的尝试点
#PG:扰动Action,不同的action带来不同的reward,通过reward大小对应上action来计算gradient,再反向传递gradient
#ES:扰动神经网络中的Parameters,不同的parameters带来不同的reward,通过reward大小对应上parameters来按比例更新原始的parameters

import numpy as np
import gym
import multiprocessing as mp
import time

N_KID = 10
N_GENERATION = 5000
LR = .05
SIGMA = .05
N_CORE = mp.cpu_count()-1#cpu核数
CONFIG = [
        dict(game='CartPole-vo', n_feature=4, n_action=2, continuous_a=[False], ep_max_step=700, eval_threshold=500),
        dict(game='MountainCar-v0', n_feature=2, n_action=3, continuous_a=[False], ep_max_step=200, eval_threshold=-120),
        dict(game='Pendulum-v0', n_feature=3, n_action=1, continuous_a=[True, 2.], ep_max_step=200, eval_threshold=-180)
        ][2]

def sign(k_id):#偶数的话是-1,奇数是1
    return -1. if 0 == k_id % 2 else 1

class SGD(object):
    def __init__(self, params, learning_rate, momentum=0.9):
        self.val = np.zeros_like(params).astype(np.float32)#(761,)
        self.lr, self.mometum = learning_rate, momentum
    
    def get_gradients(self, gradients):#动量的方式计算梯度
        self.val = self.mometum*self.val + (1. - self.mometum)*gradients
        return self.lr * self.val

def params_reshape(shapes, params):#[(3, 30), (30, 20), (20, 1)]
    p_val,start = [],0
    for index,shape in enumerate(shapes):
        n_w,n_b = shape[0]*shape[1],shape[1]
        p_val = p_val+[params[start: start+n_w].reshape(shape), params[start+n_w: start+n_w+n_b].reshape((1, shape[1]))]
        print(p_val[2*index].shape, p_val[2*index+1].shape)
        print(type(p_val[0]))
        start += n_w+n_b
    return p_val#列表中元素为np.array=>[(3, 30), (1, 30), (30, 20), (1, 20), (20, 1), (1, 1)]

def get_reward(shapes, params, env, ep_max_step, continuous_a, seed_and_id=None):#[(3, 30), (30, 20), (20, 1)], (761,), 环境, 200, [True, 2.0], [noise_seed[index], index]
    if seed_and_id is not None:
        seed,k_id = seed_and_id
        np.random.seed(seed)
        #这儿做这个是所为何
        params += sign(k_id)*SIGMA*np.random.randn(params.size)#761个标准正态分布*0.05*[+/-]1
    p_val = params_reshape(shapes, params)
    state = env.reset()#环境重置(3,)
    ep_r = 0.
    for step in range(ep_max_step):#最多尝试步数
        action = get_action(p_val, state, continuous_a)
        state, reward, done, _ = env.step(action)#执行动作之后的状态,获得的奖励以及是否完成
        if 'MountainCar' == env.spec._env_name and state[0] > -0.1:
            reward = 0.
        ep_r += reward#记录获得的奖励
        if done:
            break
    return ep_r#返回获得的奖励

def get_action(params, state, continuous_a):
    state = state[np.newaxis, :]#(1,3)
    state = np.tanh(state.dot(params[0]) + params[1])#wx+b=>(1,3)*(3*30) + (30,) = (1,30)
    state = np.tanh(state.dot(params[2]) + params[3])#(1*30)*(30*20) + (20,) = (1,20)
    state = state.dot(params[4]) + params[5]#(1,20)*(20*1) + (1,) = (1*1)
    #具体的和环境有关
    if not continuous_a[0]:
        return np.argmax(state, axis=1)[0]#求最大的index
    else:
        return continuous_a[1]*np.tanh(state)[0]#返回的是向量

def build_net():
    def linear(n_in, n_out):
        w = np.random.randn(n_in*n_out).astype(np.float32)*.1#标准正态分布
        b = np.random.randn(n_out).astype(np.float32)*.1
        return (n_in,n_out), np.concatenate((w, b))#n_in*n_out + n_out
    
    s0, p0 = linear(CONFIG['n_feature'], 30)#(3, 30)(120,)
    s1, p1 = linear(30, 20)#(30, 20)(620,)
    s2, p2 = linear(20, CONFIG['n_action'])#(20, 1)(21,)
    return [s0, s1, s2], np.concatenate((p0, p1, p2))#[(3, 30), (30, 20), (20, 1)],(761,)

def train(net_shapes, net_params, optimizer, utility, pool):
    noise_seed = np.random.randint(0, 2**32-1, size=N_KID, dtype=np.uint32).repeat(2)#0-4294967295选择10个重复2次当做噪声的种子(20,)
    #apply_async异步执行,同时启动进程池中多个进程执行事件,可以获取事件返回值
    #apply同步执行,执行完一个再执行另一个,无法获取返回值
    #多线程执行的函数是get_reward,20个job
    jobs = [pool.apply_async(get_reward, (net_shapes, net_params, env, CONFIG['ep_max_step'], CONFIG['continuous_a'], [noise_seed[k_id],k_id])) for k_id in range(N_KID*2)]
    rewards = np.array([job.get() for job in jobs])#所有的问题获得结果
    kids_rank = np.argsort(rewards)[::-1]#对20个任务按照奖励从小到大的index,[::-1]=>从大到小的index
    cumulative_update = np.zeros_like(net_params)
    for ui,k_id in enumerate(kids_rank):#先遍历的是奖励最大的job
        np.random.seed(noise_seed[k_id])
        #utility是从小到大的概率, sign(k_id)孩子的id
        cumulative_update += utility[ui]*sign(k_id)*np.random.rand(net_params.size)#均匀分布
    gradients = optimizer.get_gradients(cumulative_update/(2*N_KID*SIGMA))
    return net_params+gradients, rewards

if __name__ == '__main__':
    base = N_KID*2#20
    rank = np.arange(1, base+1)#1-20
    util_ = np.maximum(0, np.log(base/2+1)-np.log(rank))#11-20全部是0
    utility = util_/util_.sum() - 1/base#换成概率,全部减去1/n
    
    net_shapes, net_params = build_net()
    env = gym.make(CONFIG['game']).unwrapped#初始化环境
    optimizer = SGD(net_params, LR)
    #提供指定数量的进程供用户调用,有新的请求提交至Pool中时进程池尚未满创建一个新的进程来执行请求,要是满了就请求等待
    #processes默认os.cpu_count()
    #maxtasksperchild默认是None,意味只要Pool存在工作进程就一直存活
    pool = mp.Pool(processes=N_CORE)#线程池
    mar = None
    for index in range(N_GENERATION):#5000个回合
        t0 = time.time()
        net_params, kid_rewards = train(net_shapes, net_params, optimizer, utility, pool)
        net_r = get_reward(net_shapes, net_params, env, CONFIG['ep_max_step'], CONFIG['continuous_a'], None)#用新参数获得奖励
        mar = net_r if mar is None else 0.9*mar + 0.1*net_r#和老奖励的做平滑,修正
        print('Gen: ', index, '| Net_R: %.1f' % mar, '| Kid_avg_R: %.1f' % kid_rewards.mean(), '| Gen_T: %.2f' % (time.time() - t0))
        if mar >= CONFIG['eval_threshold']:#判断结束条件
            break
    p_val = params_reshape(net_shapes, net_params)
    while True:
        state = env.reset()
        for _ in range(CONFIG['ep_max_step']):
            env.render()
            a = get_action(p_val, state, CONFIG['continuous_a'])
            state, _, done, _ = env.step(a)
            if done:
                break