#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-

#dict就是map,用空间换取时间的做法,dict的key是不可变对象(哈希算法)
map0 = {"natasha": 100, "gavin": 90, "boyce": 80}
print(map0["natasha"])
#查找时写算法可以参考字典的例子
map0["yang"] = 70
print(map0["yang"])
print("yang in map0 ", "yang" in map0)
print("na in map0", "na" in map0)
print("yang = ", map0.get("yang"))
map0.pop("gavin")
print(map0)

#set是一组key值的集合,key值不能重复,要创建一个set要提供一个list作为输入集合
set0 = set([1, 2, 3])
print(set0)
#重复元素在set中是自动被过滤的
set0 = set([1, 2, 1, 2, 3, 3])
print(set0)
set0.add(4)
print(set0)
set0.add(4)
print(set0)
set0.remove(4)
print(set0)
set1 = set([1, 2, 3])
set2 = set([2, 3, 4])
print(set1 & set2)
print(set1 | set2)

#不可变对象,不可变对象调用对象自身的任意方法都不会修改该对象自身的内容,会创建新的对象并返回
array = ['c', 'b', 'a']
array.sort()
print(array)
astr = "abc"
print(astr.replace('a', 'A'))
print(astr)


