# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 09:21:32 2017

@author: natasha1_Yang
"""

from inspect import isgeneratorfunction
import types
def run():
    for index in range(1, 10):
        yield index#generator
        yield index + 100
#generator自动抛出StopIteration异常,表示迭代完成,在for循环里,无需处理StopIteration循环会正常结束
#使用isgeneratorfunction判断
#每次调用到yield返回生成器的值,下次再调用的时候从yield开始往下执行
for j in run():
    print j
    print "E"

isgeneratorfunction(run)

isinstance(run, types.GeneratorType)
isinstance(run(), types.GeneratorType)