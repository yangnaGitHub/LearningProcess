# -*- coding: utf-8 -*-
"""
Created on Tue Nov 08 09:07:05 2016

@author: natasha1_Yang
"""

def calcEM(height):
    N = len(height)
    gp = 0.5
    bp = 0.5
    gmu, gsigma = min(height), 1
    bmu, bsigma = max(height), 1
    ggamma = range(N)
    bgamma = range(N)
    cur = [gp, bp, gmu, gsigma, bmu, bsigma]
    now = []
    
    times = 0
    while times < 100:
        index = 0;
        for x in height:
            ggamma[index] = gp * gauss(x, gmu, gsigma)
            bgamma[index] = bp * gauss(x, bmu, bsigma)
            s = ggamma[index] + bgamma[index]
            ggamma[index] /= s
            bgamma[index] /= s
            index += 1
        
        gn = sum(ggamma)
        gp = float(gn) / float(N)
        bn = sum(bgamma)
        bp = float(bn) / float(N)
        gmu = averageWeight(height, ggamma, gn)
        gsigma = varianceWeight(height, ggamma, gmu, gn)
        bmu = averageWeight(height, bgamma, bn)
        bsigma = varianceWeight(height, bgamma, bmu, bn)
        
        now = [gp, bp, gmu, gsigma, bmu, bsigma]
        if isSame(cur, now):
            break
        cur = now
        print "Times:\t", times
        print "Girl mean/gsigma:\t", gmu, gsigma
        print "Boy mean/bsigma:\t", bmu, bsigma
        print "Boy/Girl:\t", bn, gn, bn+gn
        print "\n\n"
        times += 1
    return now