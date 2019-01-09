#使用线程有两种方式函数或者用类来包装线程对象
#调用_thread模块中的start_new_thread()函数来产生新线程
#_thread.start_new_thread ( function, args[, kwargs] )
import _thread
import time
import threading

def ThreadFunc(threadNo, delay):
    count = 0
    while count < 5:
        time.sleep(delay)
        count += 1
        print("%s: %s" % (threadNo, time.ctime(time.time())))
    #threadNo.exit()

try:
    _thread.strat_new_thread(ThreadFunc, ("No1", 2))
    _thread.strat_new_thread(ThreadFunc, ("No2", 3))
except:
    print("Error")

#threading.currentThread()返回当前的线程变量
#threading.enumerate()包含正在运行的线程的list
#threading.activeCount()返回正在运行的线程数量=len(threading.enumerate())
#run()表示线程活动的方法
#start()启动线程活动
#join([time])等待至线程中止,阻塞调用线程直至线程的join()方法被调用中止
#isAlive()线程是否活动的
#getName()返回线程名
#setName()设置线程名
#通过直接从threading.Thread继承创建一个新的子类,实例化后调用start()方法启动新线程

class myThread(threading.Thread):
    def __init__(self, threadNo, name, counter):
        threading.Thread.__init__(self)
        self.threadNo = threadNo
        self.name = name
        self.counter = counter
    def run(self):
        print("start: " + self.name)
        #threadLock.acquire()
        ThreadFunc(self.name, self.counter)
        #threadLock.release()
        print("end: " + self.name)

thread1 = myThread(1, "No1", 2)
thread2 = myThread(2, "No2", 3)
thread1.start()
thread2.start()
thread1.join()
thread2.join()
#threads.append(thread1)#添加线程到线程列表
#threads.append(thread2)
#for t in threads:#等待所有线程完成
#    t.join()

#Lock和Rlock可以实现简单的线程同步,两个对象都有acquire和release,需要每次只允许一个线程操作的数据,将其操作放到放到之间

#Queue模块中提供了同步的线程安全的队列类FIFO+LIFO+PriorityQueue
#Queue.qsize()返回队列的大小
#Queue.empty()
#Queue.full()
#Queue.get([block[, timeout]])获取队列
#Queue.get_nowait()相当Queue.get(False)
#Queue.put(item)写入队列
#Queue.put_nowait(item)=Queue.put(item, False)
#Queue.task_done()完成一项工作之后向任务已经完成的队列发送一个信号
#Queue.join()意味着等到队列为空再执行别的操作










