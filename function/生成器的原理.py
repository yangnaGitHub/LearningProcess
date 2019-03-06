# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 17:26:29 2019

@author: natasha_yang

@e-mail: ityangna0402@163.com
"""

#当一个python函数调用子程序的时候,这个子程序一直持有控制权,只有当子程序结束后,控制权才还给调用者
#标准的python解释器是用C写的,解释器用一个PyEval_EvalFrameEx的C函数来执行Python函数
#堆栈帧,函数调用栈当中的某一帧,相当于一个上下文,接受一个Python的堆栈帧对象,并在这个堆栈帧的上下文中执行Python的字节码
#python一切皆对象,栈帧也是一个对象

def foo():
    bar()

def bar():
    pass

import dis#dis模块查看编译后的字节码
print(dis.dis(foo))
#  2           0 LOAD_GLOBAL              0 (bar)  ==> 把bar这个函数给load进来
#              2 CALL_FUNCTION            0        ==> 调用bar函数的字节码
#              4 POP_TOP                           ==> 从栈的顶端把元素打印出来
#              6 LOAD_CONST               0 (None) ==> 我们这里没有return,所以会把None给load进来
#              8 RETURN_VALUE                      ==>把None给返回
#先预编译,得到字节码对象
#python解释器去解释字节码
#当解释到foo函数的字节码时,会为其创建一个栈帧
#然后调用C函数PyEval_EvalFrameEx()在foo对应的栈帧上执行foo的字节码,参数就是foo对应的栈帧对象
#当遇到CALL_FUNCTION,也就是在foo中执行到bar的字节码时,会继续为其创建一个栈帧
#然后把控制权交给新创建的栈帧对象,在bar对应的栈帧中运行bar的字节码
#关键所有的栈帧都分配在堆的内存(不释放一直存在)上,而不是栈的内存上,堆内存决定了栈帧可以独立于调用者存在,调用者不存在或者退出函数也没有关系

import inspect#可以获取栈帧
frame = None
def foo_1():
    bar_1()

def bar_1():
    global frame
    #栈帧对象一般有三个属性f_back当前栈帧的上一级栈帧,f_code当前栈帧对应的字节码,f_locals当前栈帧所用的局部变量
    frame = inspect.currentframe()#将获取到的栈帧对象赋给全局变量
foo_1()
print(frame.f_code)
print(frame.f_code.co_name)
#可以拿到foo的栈帧
foo_1_frame = frame.f_back
print(foo_1_frame.f_code)
print(foo_1_frame.f_code.co_name)

#栈帧是分配在堆内存上的,生成器才有实现的可能
#调用一个生成器函数时,Python会看到生成器的标志,实际上并不运行该函数而是创建一个生成器
#python生成器封装了一个堆栈帧和一个对生成器函数代码的引用
def gen_fn():
    result = yield 1
    print('result of yield: {}'.format(result))
    result2 = yield 2
    print('result of 2nd yield: {}'.format(result2))
    return 'done'
#gi_frame->(f_lasti+f_locals)
#gi_code->(f_code)
gen = gen_fn()
print(type(gen))#<class 'generator'>
print(dis.dis(gen))#YIELD_VALUE
#  2           0 LOAD_CONST               1 (1)
#              2 YIELD_VALUE
#              4 STORE_FAST               0 (result)
#
#  3           6 LOAD_GLOBAL              0 (print)
#              8 LOAD_CONST               2 ('result of yield: {}')
#             10 LOAD_ATTR                1 (format)
#             12 LOAD_FAST                0 (result)
#             14 CALL_FUNCTION            1
#             16 CALL_FUNCTION            1
#             18 POP_TOP
#
#  4          20 LOAD_CONST               3 (2)
#             22 YIELD_VALUE
#             24 STORE_FAST               1 (result2)
#
#  5          26 LOAD_GLOBAL              0 (print)
#             28 LOAD_CONST               4 ('result of 2nd yield: {}')
#             30 LOAD_ATTR                1 (format)
#             32 LOAD_FAST                1 (result2)
#             34 CALL_FUNCTION            1
#             36 CALL_FUNCTION            1
#             38 POP_TOP
#
#  6          40 LOAD_CONST               5 ('done')
#             42 RETURN_VALUE
#堆栈帧有个last instruction,指向最近执行的那条指令,刚开始的时候指针是-1,意味着生成器尚未开始
print(gen.gi_frame.f_lasti)
print(gen.gi_frame.f_locals)
next(gen)
print(gen.gi_frame.f_lasti)
print(gen.gi_frame.f_locals)
next(gen)
print(gen.gi_frame.f_lasti)
print(gen.gi_frame.f_locals)
#对函数的暂停和前进,进行了完美的监督,有变量保存我最近一行代码执行到什么位置,再通过yield来暂停它,就实现了我们的生成器
#yield关键字实际返回一个IteratorResult对象
#value和done,value属性是对yield表达式求值的结果,done是生成器函数尚未完全完成
#生成器的执行结束,并且IteratorResult给调用者返回undefined并且done为true

#生成器方式的斐波那锲函数
def fib(number):
    index, x_data, x_1_data = 0, 0, 1
    while index < number:
        yield x_1_data#返回值
        x_data, x_1_data = x_1_data, x_data+x_1_data 
        index += 1

print([data for data in fib(6)])