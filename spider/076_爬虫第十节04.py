# -*- coding: utf-8 -*-
"""
Created on Thu May 25 10:33:00 2017

@author: natasha1_Yang
"""

from tesserocr import PyTessBaseAPI, RIL, iterate_level

with PyTessBaseAPI() as api:
    api.SetImageFile('vali-1.png')
    api.SetVariable('save_blob_choices', 'T')
    api.Recognize()
    
    ri = api.GetIterator()
    level = RIL.SYMBOL
    for r in iterate_level(ri, level):
        symbol = r.GetUTF8Text(level)
        conf = r.Confidence(level)
        if symbol:
            print u'symbol {}, conf: {}'.format(symbol, conf)
        indent = False
        ci = r.GetChoiceIterator()
        for c in ci:
            if indent:
                print '\t\t '
            print '\t- '
            choice = c.GetUTF8Text()
            print u'{} conf: {}'.format(choice, c.Confidence)