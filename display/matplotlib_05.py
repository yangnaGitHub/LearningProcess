# -*- coding: utf-8 -*-
"""
Created on Thu Jan 10 15:32:53 2019

@author: natasha_yang

@e-mail: ityangna0402@163.com
"""

import matplotlib.pyplot as plt
import numpy as np

x_data = np.array([0.313660827978, 0.365348418405, 0.423733120134,
                   0.365348418405, 0.439599930621, 0.525083754405,
                   0.423733120134, 0.525083754405, 0.651536351379]).reshape(3,3)
plt.imshow(x_data, interpolation='nearest', cmap='bone', origin='lower')#origin选择的原点的位置
#添加colorbar,colorbar的长度变短为原来的92%
plt.colorbar(shrink=.92)

plt.xticks(())
plt.yticks(())
plt.show()


methods = [None, 'none', 'nearest', 'bilinear', 'bicubic', 'spline16',
           'spline36', 'hanning', 'hamming', 'hermite', 'kaiser', 'quadric',
           'catrom', 'gaussian', 'bessel', 'mitchell', 'sinc', 'lanczos']
np.random.seed(0)
grid = np.random.rand(4, 4)

fig, axes = plt.subplots(3, 6, figsize=(12, 6), subplot_kw={'xticks': [], 'yticks': []})
fig.subplots_adjust(hspace=0.3, wspace=0.05)

for ax, interp_method in zip(axes.flat, methods):
    ax.imshow(grid, interpolation=interp_method, cmap='viridis')
    ax.set_title(interp_method)
plt.show()