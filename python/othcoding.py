#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
#函数可以当作返回值,返回一个函数时，牢记该函数并未执行
def calc_sum(*args):
    ax = 0
    for count in args:
        ax = ax + count
    return ax
#内部函数sum可以引用lazy_sum的参数和局部变量
def lazy_sum(*args):
    def sumfun():
        ax = 0
        for count in args:
            ax = ax + count
        return ax
    return sumfun
fun = lazy_sum(1, 2, 3, 4, 5)
print(fun())

#闭包,返回函数不要引用任何循环变量，或者后续会发生变化的变量
def countfun():
    fs = []
    for index in range(1, 4):
        def fun():
            return index * index
        fs.append(fun)
    return fs
fun1, fun2, fun3 = countfun()
#引用的index已经变成了3
print(fun1(), " ", fun2(), " ", fun3())
def othcount():
    def fun(args):
        def gfun():
            return args * args
        return gfun
    fs = []
    for index in range(1, 4):
        fs.append(fun(index))
    return fs
fun1, fun2, fun3 = othcount()
print(fun1(), " ", fun2(), " ", fun3())
#返回3个函数,即fun1 = fs[1], fun2 = fs[2], fun3 = fs[3]
#fun1()-->fs[1]()-->fun(1)-->1 * 1

#匿名函数,有限的支持lambda,匿名函数只有一个表达式,不用写return
print(list(map(lambda xval: xval * xval, [1, 2, 3, 4, 5, 6, 7, 8, 9])))


