# -*- coding: utf-8 -*-
"""
Created on Thu May 25 10:21:35 2017

@author: natasha1_Yang
"""

from tesserocr import PyTessBaseAPI

images = ['test.jpg', 'test2.jpg', 'vali-2.jpeg', 'vali-1.png']

with PyTessBaseAPI() as api:
    for img in images:
        print 'file: ' + img
        api.SetImageFile(img)
        print 'result: ' + api.GetUTF8Text()
        print 'confidence: '
        print api.AllWordConfidences()