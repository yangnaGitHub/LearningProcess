#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
def fact(count):
    if count == 1:
        return 1
    return count * fact(count - 1)

print(fact(5))
#递归调用可能会导致栈溢出,尾递归优化可以解决这个问题(尾递归=循环)
#尾递归函数中返回不带表达式的函数的本身
#尾递归的时候如果做了优化,栈不会增长,所以不会导致栈溢出
#python解释器并没有做优化,所以仍旧会溢出
def factmod(count):
    return fact_iter(count, 1)
def fact_iter(num, product):
    if num == 1:
        return product
    return fact_iter(num - 1, num * product)

def move(count, diska, diskb, diskc):
    if count == 1:
        print(diska, "==>", diskc)
        return
    move(count - 1, diska, diskc, diskb)
    move(1, diska, diskb, diskc)
    move(count - 1, diskb, diska, diskc)

print(move(4, "A", "B", "C"))
#print(move(1, "A", "B", "C"))



