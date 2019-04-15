#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
x = b'ABC'
print("x = ", x)
print("ascii = ", 'BCD'.encode('ascii'))
print("utf8 = ", 'BCD'.encode('utf-8'))
print("杨娜utf8 = ", '杨娜'.encode('utf-8'))
print("to ascii = ", b'ABC'.decode('ascii'))
print("\'ABC\' len = ", len('ABC'))
print("\'杨娜\' len = ", len('杨娜'))
print("\'杨娜\' len = ", len('杨娜'.encode('utf-8')))
print("hi, %s, you have $%d." % ("natasha", 1000))
print("%02d-%02d" % (3, 1))
print("growth rate: %d %%" % 7)
s1 = 72
s2 = 85
r = (s2 - s1) / s1
print("%3.1f" % r)
