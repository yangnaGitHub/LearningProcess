#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
#�������������ĵ�ʱ��,������������仰�Ǵ����
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
#tupleһ����ʼ���Ͳ��ܸ���,�ڶ���tubleʱֵ�ͻᱻȷ������,���Դ������ȫ
myclass = ('natasha', 'jet', 'zain')
print(myclass)
test = (1, )#һ��Ԫ��ʱҪ��������
print(test)
#ָ�򲻱�
mytest = ('natasha', 'mark', ['yang', 'na'])
print(mytest)
mytest[2][0] = 'nana'
print(mytest)

