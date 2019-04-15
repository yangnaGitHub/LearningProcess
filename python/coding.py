#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
#由于abs函数实际上是定义在__builtin__模块中的，所以要让修改abs变量的指向在其它模块也生效，要用__builtin__.abs = 10
#一个函数就接收另一个函数作为参数，这种函数就称之为高阶函数
def add_abs(xval, yval, fun):
	return fun(xval) + fun(yval)
print(add_abs(-5, 6, abs))
#Python内建了map()和reduce()函数
#map()函数接收两个参数，一个是函数，一个是Iterable，map将传入的函数依次作用到序列的每个元素，并把结果作为新的Iterator返回
def sec(count):
	return count * count
result = map(sec, list(range(1, 11)))#result is Iterator
print(list(result))
print(list(map(str, list(range(1, 10)))))
#reduce把一个函数作用在一个序列[x1, x2, x3, ...]上，这个函数必须接收两个参数，reduce把结果继续和序列的下一个元素做累积计算
#reduce(f, [x1, x2, x3, x4]) = f(f(f(x1, x2), x3), x4)
from functools import reduce
def oth_add(xval, yval):
	return xval + yval
print(reduce(oth_add, [index for index in range(10) if index % 2 != 0]))
def integret(xval, yval):
	return xval * 10 + yval
print(reduce(integret, [index for index in range(10) if index % 2 != 0]))
def char2int(str):
	return {"0":0, "1":1, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9}[str]
print(reduce(integret, map(char2int, "13579")))
def str2int(str):
	return reduce(lambda xval, yval: xval * 10 + yval, map(char2int, str))
print(str2int("12345"))
def upper(mystr):
	return mystr[0].upper() + mystr[1:].lower()
result = map(upper, ["natasha", "yAng", "NA"])
print(list(result))
print(reduce(lambda xval, yval: xval + yval, [3, 5, 7, 9]))
char_to_float = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '.': -1}
num = map(lambda ch: char_to_float[ch], "123.45")
def cove(strnum):
    point = 0
    def str2float(floatnum, count):
        nonlocal point#nonlocal的应用
        if count == -1:
            point = 1
            return floatnum
        if point == 0:
            return floatnum * 10 + count
        else:
            point = point * 10
            return floatnum + count / point
    print(reduce(str2float, strnum, 0.0))
cove(num)
#filter
#Python内建的filter()函数用于过滤序列
#filter()也接收一个函数和一个序列,filter()把传入的函数依次作用于每个元素，然后根据返回值是True还是False决定保留还是丢弃该元素
def is_odd(num):
    return num % 2 == 1
print(list(filter(is_odd, list(range(1, 16)))))
def not_empty(strnum):
    return strnum and strnum.strip()
print(list(filter(not_empty, ["A", None, "B", "", " ", "C"])))
#3开始的奇数序列
def _odd_iter():
    count = 1
    while True:
        count = count + 2
        yield count
#filter函数,取出count的倍数
def _not_divisible(count):
    return lambda xval: xval % count > 0
def primes():
    yield 2#输出2
    it = _odd_iter()
    while True:
        count = next(it)
        yield count#输出3等素数
        it = filter(_not_divisible(count), it)
for index in primes():
    if index < 1000:
       print(index)
    else:
        break
def is_palindrome(num):
    strnum = str(num)
    index, maxlen = 0, len(strnum) - 1
    while index < maxlen:
        if strnum[index] != strnum[maxlen]:
            return False
        index = index + 1
        maxlen = maxlen - 1
    return num
print(list(filter(is_palindrome, [12321, 12345, 232, 23452, 909])))
#Python内置的sorted()函数就可以对list进行排序
print(sorted([79, 21, 19, 45, 43]))
#可以接收一个key函数来实现自定义的排序
print(sorted([-79, -21, 19, 45, 43], key = abs))
print(sorted(["yangna", "natasha", "nancy", "twilight"]))
print(sorted(["Yangna", "Natasha", "nancy", "twilight"], key = str.lower))
print(sorted(["yangna", "natasha", "nancy", "twilight"], key = str.lower, reverse = True))
#用sorted()排序的关键在于实现一个映射函数
def by_name(List):
    temp, result = [], []
    index, maxlen = 0, len(List)
    tag, count = 0, 0
    while index < maxlen:
        temp.append(List[index][0])
        index = index + 1
    temp = sorted(temp)
    index, maxlen = 0, len(temp)
    while index < maxlen:
        tag, count = 0, len(List)
        while tag < count:
            if temp[index] == List[tag][0]:
                result.append(List[tag])
                List.pop(tag)
                break
            tag = tag + 1
        index = index + 1
    return result
Mylist = [("yangna", 100), ("natasha", 90), ("nancy", 80), ("twilight", 70)]
#print(sorted(Mylist, key = by_name))
print(by_name(Mylist))
