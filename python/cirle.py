#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
def fact(count):
    if count == 1:
        return 1
    return count * fact(count - 1)

print(fact(5))
#�ݹ���ÿ��ܻᵼ��ջ���,β�ݹ��Ż����Խ���������(β�ݹ�=ѭ��)
#β�ݹ麯���з��ز������ʽ�ĺ����ı���
#β�ݹ��ʱ����������Ż�,ջ��������,���Բ��ᵼ��ջ���
#python��������û�����Ż�,�����Ծɻ����
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



