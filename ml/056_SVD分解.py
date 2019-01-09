# -*- coding: utf-8 -*-
"""
Created on Wed Mar 08 15:47:17 2017

@author: natasha1_Yang
"""

from PIL import Image
import numpy as np

def restore(sigma, u, v, index):
    m = len(u)
    n = len(v[0])
    array = np.zeros((m, n))
    for mindex in range(index + 1):
        for nindex in range(m):
            array[nindex] += sigma[mindex] * u[nindex][mindex] * v[mindex]
    temp = array.astype("uint8")
    return temp  

if __name__ == "__main__":
    im = Image.open("056_PIC.jpg")
    imarray = np.array(im)
    #分离通道
    R, G, B = im.split()
    imR = np.array(R)#imarray[:,:,0]
    imG = np.array(G)#imarray[:,:,1]
    imB = np.array(B)#imarray[:,:,2]
    
    #imarray.shape = (960, 3840)
    #reimarray = imarray.reshape((960, 3840))
    #不需要imarray.transpose()转置
    result = np.zeros(imarray.shape, dtype="uint8")
    output_path = '.\\056_SVDPIC'
   
    RU, Rsigma, RV = np.linalg.svd(imR, full_matrices=False)
    GU, Gsigma, GV = np.linalg.svd(imG, full_matrices=False)
    BU, Bsigma, BV = np.linalg.svd(imB, full_matrices=False)
    for index in np.linspace(10, 700, 10):
        index = int(index)
        RE = restore(Rsigma, RU, RV, index)
        GE = restore(Gsigma, GU, GV, index)
        BE = restore(Bsigma, BU, BV, index)
        result[:, :, 0] = RE
        result[:, :, 1] = GE
        result[:, :, 2] = BE
        Image.fromarray(result).save(output_path + ("\\tempsvd_" + str(index) + ".jpg"))