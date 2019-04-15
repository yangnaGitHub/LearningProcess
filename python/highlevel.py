#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
#切片List + tuple + string
List = ["natasha", "yang", "na", "nancy"]
print([List[0], List[1]])
print(List[0:2])
print(List[:2])
print(List[1:2])
print(List[-2:])
print(List[-2:-1])
Num = list(range(100))
print(Num[10:20])
print(Num[:10:2])
print(Num[::5])
#copy Num[:]

#迭代==遍历dict==>value+d.values && key,value+d.items
#判断一个对象是否是可以迭代的collections模块的iterable
from collections import Iterable
print(isinstance('abc', Iterable))
#Python内置的enumerate函数可以把一个list变成索引-元素对
#List = ["A", "B", "C"]在用过enumerate函数后key = 0, value = "A"以此类推

#列表生成式
List = [x * x for x in range(1, 11)]
print(List)
List = [x * x for x in range(1, 11) if x % 2 == 0]
print(List)
List = [m + n for m in "ABC" for n in "abc"]
print(List)
import os
List = [dir for dir in os.listdir(".")]
print(List)
dic = {"yang": "21", "fang": "19", "ling": "43"}#string
List = [k + "=" + v for k, v in dic.items()]
print(List)
List = ['Yang', 'Na', 'Natasha']
print([s.lower() for s in List])
List = ['Yang', 18, 'Na', 'Natasha']
print([s.lower() for s in List if isinstance(s, str)])

#一边循环一边计算的机制叫做生成器,生成器保存的是算法
gist = (x * x for x in range(10))
print(next(gist), next(gist), next(gist), next(gist), next(gist))
#print(gist)
def fib(max):
    index, pre, later = 0, 0, 1
    while index < max:
        print(later)
        pre, later = later, pre + later
        index = index + 1
    return "done" 
print(fib(3), fib(4), fib(5))
#如果一个函数定义中包含yield关键字，那么这个函数就不再是一个普通函数
def fib_gen(max):
    index, pre, later = 0, 0, 1
    while index < max:
        yield later
        pre, later = later, pre + later
        index = index + 1
    return "done" 
#generator的函数，在每次调用next()的时候执行，遇到yield语句返回，再次执行时从上次返回的yield语句处继续执行
mode = fib_gen(5)
print(next(mode), next(mode), next(mode), next(mode), next(mode))
#拿不到generator的return语句的返回值。如果想要拿到返回值，必须捕获StopIteration错误，返回值包含在StopIteration的value中
#generator函数的“调用”实际返回一个generator对象
mode = fib_gen(5)
while True:
    try:
        val = next(mode)
        print(val)
    except StopIteration as e:
        print("return Value: ", e.value)
        break

def triangles(List):
    temp = []
    index, maxnum = 0, len(List)
    while index < maxnum:
        if index == 0:
            temp.append(1)
        else:
            temp.append(List[index] + List[index - 1])
        index = index + 1
    temp.append(1)
    return temp
def Calltriang(number):
    index, maxnum = 1, 0
    List, temp = [1,], []
    print(List)
    while index < number:
        temp = triangles(List)
        yield temp
        List = temp
        index = index + 1
    return "done"
mode = Calltriang(6)
while True:
    try:
        val = next(mode)
        print(val)
    except StopIteration as e:
        print("return Value: ", e.value)
        break
#迭代器，可以直接作用于for循环的对象统称为可迭代对象：Iterable
#list、tuple、dict、set、str、generator、带yield的generator function
#可以使用isinstance()判断一个对象是否是Iterable对象
from collections import Iterable
print(isinstance([], Iterable))
print(isinstance({}, Iterable))
print(isinstance("100", Iterable))
#可以被next()函数调用并不断返回下一个值的对象称为迭代器：Iterator
#可以使用isinstance()判断一个对象是否是Iterator对象
from collections import Iterator
print(isinstance([], Iterator))
print(isinstance({}, Iterator))
print(isinstance("100", Iterator))
print(isinstance((x for x in range(10)), Iterator))
#生成器都是Iterator对象，但list、dict、str虽然是Iterable，却不是Iterator
#把list、dict、str等Iterable变成Iterator可以使用iter()函数
print(isinstance(iter([]), Iterator))
print(isinstance(iter({}), Iterator))
print(isinstance(iter("100"), Iterator))
#Python的Iterator对象表示的是一个数据流，Iterator对象可以被next()函数调用并不断返回下一个数据，直到没有数据时抛出StopIteration错误
#可以把这个数据流看做是一个有序序列，但我们却不能提前知道序列的长度，只能不断通过next()函数实现按需计算下一个数据，所以Iterator的计算是惰性的，只有在需要返回下一个数据时它才会计算
#小结
#可作用于for循环的对象都是Iterable类型
#可作用于next()函数的对象都是Iterator类型
#集合数据类型如list、dict、str等是Iterable但不是Iterator，可以通过iter()函数获得一个Iterator对象
#Python的for循环本质上就是通过不断调用next()函数实现的