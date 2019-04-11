# -*- coding: utf-8 -*-
'''
Created on Wed Mar  6 17:53:45 2019

@author: yangna

@e-mail: ityangna0402@163.com
'''

import threading
import time

####1
def thread_job():
    print('T1 start\n')
    for index in range(10):
        time.sleep(0.1)#sleep 0.1s
    print('T1 finish\n')

added_thread = threading.Thread(target=thread_job, name='T1')
added_thread.start()

#print('done')#线程任务还未完成便输出

added_thread.join()
print('done')##线程任务完成才会输出

####2
def thread_job_t1():
    print('T1 start\n')
    for index in range(10):
        time.sleep(0.1)#sleep 0.1s
    print('T1 finish\n')
    
def thread_job_t2():
    print('T2 start\n')
    print('T2 finish\n')

thread_1 = threading.Thread(target=thread_job_t1, name='T1')
thread_2 = threading.Thread(target=thread_job_t2, name='T2')

#thread_1.start()
#thread_2.start()
#print('done')

#thread_1.start()
#thread_1.join()#第一个完成才会做下面的
#thread_2.start()
#print('done')

#1221形式
thread_1.start()
thread_2.start()
thread_2.join()
thread_1.join()
print('done')