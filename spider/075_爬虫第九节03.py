# -*- coding: utf-8 -*-
"""
Created on Tue May 23 15:07:11 2017

@author: natasha1_Yang
"""

import heapq
from collections import defaultdict

def encode(frequency):
    heap = [[weight, [symbol, '']] for symbol, weight in frequency.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        print lo, hi
        print "natasha: ", lo[0], hi[0], lo[1:], hi[1:]
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    return sorted(heapq.heappop(heap)[1:], key=lambda p: (len(p[-1]), p))

data = [64,64,64,62,62,63,61,59,58,58,59,60,60,30,32,69,58,58,59,61,64,62,62,62,63,63,63,59]

frequency = defaultdict(int)

for symbol in data:
    frequency[symbol] += 1

huff = encode(frequency)
#ljust(10)==>一共占10个字符位==>对应的是rjust
print "Symbol".ljust(10) + "Weight".ljust(10) + "Huffman Code"

for p in huff:
    print str(p[0]).ljust(10) + str(frequency[p[0]]).ljust(10) + p[1]