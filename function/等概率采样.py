# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 18:10:19 2019

@author: natasha_yang

@e-mail: ityangna0402@163.com
"""

从n个元素中随机抽取k个元素,但是n的个数无法事先确认
开始:先选取n个元素中的前k个元素,保存在集合A中
1.从第j[k+1,n]个元素开始的,每次以概率k/j选择是否让第j个元素留下=>是否替换
2.若第j个元素存活,则从A中随机选择一个元素被j替换,否则第j个元素淘汰=>替换谁

证明:
t1:在原来的n个元素中每一个最后存活下来的p = k/n(每个元素被抽中的概率)
t2:在第i[0,n-k]轮中,第k+0~k+i个元素每一个存活下来的p = k/k+i
当i=0的时候,结论成立
针对第k+i个元素,t1知道留下的概率是k/k+i
针对元素a[1,k+i)有留下有2种情况,1:第k+i个元素直接被淘汰,2:第k+i个元素留下,但是没有替换掉元素a
 归纳假设对i-1成立
 k/k+i-1[前提是第k+i-1自己存活下来] * (i/k+i[第k+i个元素直接被淘汰] + (k/k+i[第k+i个元素留下] * k-1/k[没有替换掉第第k+i-1个元素])) = k/k+i