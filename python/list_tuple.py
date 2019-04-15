#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
#当代码中有中文的时候,不加上面的两句话是错误的
classmates = ['natasha', 'bob', 'byoce']
print(classmates)
print(len(classmates))
print(classmates[0], classmates[-1], classmates[-3])
classmates.append("gavin")
print(classmates)
classmates.insert(1, "alex")
print(classmates)
classmates.pop()
print(classmates)
classmates.pop(1)
print(classmates)
classmates[1] = "yang"
print(classmates)

List = ['yang', 123, True]
print(List)
string = [['c', 'c++', 'c#'], 'java', 'python']
print(string)
print(string[0][1])
#tuple一旦初始化就不能更改,在定义tuble时值就会被确定下来,所以代码更安全
myclass = ('natasha', 'jet', 'zain')
print(myclass)
test = (1, )#一个元素时要这样定义
print(test)
#指向不变
mytest = ('natasha', 'mark', ['yang', 'na'])
print(mytest)
mytest[2][0] = 'nana'
print(mytest)

