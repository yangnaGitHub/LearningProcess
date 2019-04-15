#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
#��ƬList + tuple + string
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

#����==����dict==>value+d.values && key,value+d.items
#�ж�һ�������Ƿ��ǿ��Ե�����collectionsģ���iterable
from collections import Iterable
print(isinstance('abc', Iterable))
#Python���õ�enumerate�������԰�һ��list�������-Ԫ�ض�
#List = ["A", "B", "C"]���ù�enumerate������key = 0, value = "A"�Դ�����

#�б�����ʽ
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

#һ��ѭ��һ�߼���Ļ��ƽ���������,��������������㷨
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
#���һ�����������а���yield�ؼ��֣���ô��������Ͳ�����һ����ͨ����
def fib_gen(max):
    index, pre, later = 0, 0, 1
    while index < max:
        yield later
        pre, later = later, pre + later
        index = index + 1
    return "done" 
#generator�ĺ�������ÿ�ε���next()��ʱ��ִ�У�����yield��䷵�أ��ٴ�ִ��ʱ���ϴη��ص�yield��䴦����ִ��
mode = fib_gen(5)
print(next(mode), next(mode), next(mode), next(mode), next(mode))
#�ò���generator��return���ķ���ֵ�������Ҫ�õ�����ֵ�����벶��StopIteration���󣬷���ֵ������StopIteration��value��
#generator�����ġ����á�ʵ�ʷ���һ��generator����
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
#������������ֱ��������forѭ���Ķ���ͳ��Ϊ�ɵ�������Iterable
#list��tuple��dict��set��str��generator����yield��generator function
#����ʹ��isinstance()�ж�һ�������Ƿ���Iterable����
from collections import Iterable
print(isinstance([], Iterable))
print(isinstance({}, Iterable))
print(isinstance("100", Iterable))
#���Ա�next()�������ò����Ϸ�����һ��ֵ�Ķ����Ϊ��������Iterator
#����ʹ��isinstance()�ж�һ�������Ƿ���Iterator����
from collections import Iterator
print(isinstance([], Iterator))
print(isinstance({}, Iterator))
print(isinstance("100", Iterator))
print(isinstance((x for x in range(10)), Iterator))
#����������Iterator���󣬵�list��dict��str��Ȼ��Iterable��ȴ����Iterator
#��list��dict��str��Iterable���Iterator����ʹ��iter()����
print(isinstance(iter([]), Iterator))
print(isinstance(iter({}), Iterator))
print(isinstance(iter("100"), Iterator))
#Python��Iterator�����ʾ����һ����������Iterator������Ա�next()�������ò����Ϸ�����һ�����ݣ�ֱ��û������ʱ�׳�StopIteration����
#���԰����������������һ���������У�������ȴ������ǰ֪�����еĳ��ȣ�ֻ�ܲ���ͨ��next()����ʵ�ְ��������һ�����ݣ�����Iterator�ļ����Ƕ��Եģ�ֻ������Ҫ������һ������ʱ���Ż����
#С��
#��������forѭ���Ķ�����Iterable����
#��������next()�����Ķ�����Iterator����
#��������������list��dict��str����Iterable������Iterator������ͨ��iter()�������һ��Iterator����
#Python��forѭ�������Ͼ���ͨ�����ϵ���next()����ʵ�ֵ�