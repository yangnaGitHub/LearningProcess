# -*- coding: utf-8 -*-
"""
Created on Sat Feb 25 16:54:25 2017

@author: natasha1_Yang
"""

#问题:求体积最大的长方体的体积
#若是没有任何的限制条件是无法求的
#限制条件:表面积为a^2
#拉格朗日:函数z = f( x, y )在附加条件φ(x, y) = 0下的可能极值点
#拉格朗日函数L(x,y) = f(x, y) + λφ(x,y)
#解:长宽高==>x, y, z
#    限制条件就是2xy + 2xz + 2yz = a^2==>φ(x,y)=2xy + 2xz + 2yz - a^2 = 0
#    而要求:f(x, y) = xyz
#    L(x,y) = xyz - λ(2xy + 2xz + 2yz - a^2)
#    分别对x, y, z求导等于0,然后联立上面的式子就可以求得 