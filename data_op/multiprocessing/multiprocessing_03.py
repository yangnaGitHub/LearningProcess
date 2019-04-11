# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 10:22:28 2019

@author: yangna

@e-mail: ityangna0402@163.com
"""

#只有共享内存才能让CPU之间有交流
import multiprocessing as mp

#Shared Value
#可以通过使用Value数据存储在一个共享的内存表中
#d和i参数用来设置数据类型的,https://docs.python.org/3.5/library/array.html
#'b'	signed char	int	1	 
#'B'	unsigned char	int	1	 
#'u'	Py_UNICODE	Unicode character	2
#'h'	signed short	int	2	 
#'H'	unsigned short	int	2	 
#'i'	signed int	int	2	 
#'I'	unsigned int	int	2	 
#'l'	signed long	int	4	 
#'L'	unsigned long	int	4	 
#'q'	signed long long	int	8
#'Q'	unsigned long long	int	8
#'f'	float	float	4	 
#'d'	double	float 	8
#value1 = mp.Value('i', 0)#带符号的整型
#value2 = mp.Value('d', 3.14)#双精度浮点

#Shared Array
#Array类,可以和共享内存交互,来实现在进程之间共享数据
#array = mp.Array('i', [1, 2, 3, 4])

import time

def job(v, num):
    for _ in range(5):
        time.sleep(0.1) #暂停0.1秒,让输出效果更明显
        v.value += num # v.value获取共享变量值
        print(v.value)
        
def multicore():
    v = mp.Value('i', 0) # 定义共享变量
    p1 = mp.Process(target=job, args=(v, 1))
    p2 = mp.Process(target=job, args=(v, 3)) # 设定不同的number看如何抢夺内存
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    
if __name__ == '__main__':
    multicore()