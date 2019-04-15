#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
#如果发生了错误，可以事先约定返回一个错误代码
def foo():
    r = some_function()
    if r == (-1):
        return (-1)
    return r
def bar():
    r = foo()
    if r == (-1):
        print("Error")
    else:
        pass
#某些代码可能会出错时，就可以用try来运行这段代码，如果执行出错，则后续代码不会继续执行，而是直接跳转至错误处理代码，即except语句块，执行完except后，如果有finally语句块，则执行finally语句块
#由于没有错误发生，所以except语句块不会被执行，但是finally如果有，则一定会被执行
#可以有多个except来捕获不同类型的错误
try:
    print("try")
    r = 10 / 0
    print("result = ", r)
except ZeroDivisionError as e:
    print("except:", e)
finally:
    print("finally")
print("END")
#Python所有的错误都是从BaseException类派生的
#try...except捕获错误还有一个巨大的好处，就是可以跨越多层调用，比如函数main()调用foo()，foo()调用bar()，结果bar()出错了，这时，只要main()捕获到了，就可以处理
def foo(s):
    return 10 / int(s)
def bar(s):
    return foo(s) * 2
def main():
    try:
        bar("0")
    except Exception as e:
        print("Error : ", e)
    finally:
        print("finally")
main()
#如果错误没有被捕获，它就会一直往上抛，最后被Python解释器捕获，打印一个错误信息，然后程序退出
#Python内置的logging模块可以非常容易地记录错误信息
#import logging
#def foo(s):
#    return 10 / int(s)
#def bar(s):
#    return foo(s) * 2
#def main():
#    try:
#        bar("0")
#    except Exception as e:
#        logging.exception(e)
#main()
#raise语句抛出一个错误的实例
#凡是用print()来辅助查看的地方，都可以用断言（assert）来替代
#assert n != 0, 'n is zero!' ==> 表达式n != 0应该是True，否则，根据程序运行的逻辑
#动Python解释器时可以用-O参数来关闭assert python3.4 -O err.py
#import logging
#logging.basicConfig(level=logging.INFO)
#s = "0"
#n = int(s)
#logging.info("n = %d" % n)
print(10 / n)
#允许你指定记录信息的级别，有debug，info，warning，error等几个级别，当我们指定level=INFO时，logging.debug就不起作用了
#启动Python的调试器pdb，让程序以单步方式运行，可以随时查看运行状态
#python3 -m pdb err.py
#输入命令l来查看代码, 输入命令n可以单步执行代码, 输入命令p 变量名来查看变量, 输入命令q结束调试
#import pdb，然后，在可能出错的地方放一个pdb.set_trace()，就可以设置一个断点
#程序会自动在pdb.set_trace()暂停并进入pdb调试环境，可以用命令p查看变量，或者用命令c继续运行
