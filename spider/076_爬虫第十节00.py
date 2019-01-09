# -*- coding: utf-8 -*-
"""
Created on Tue May 23 17:07:10 2017

@author: natasha1_Yang
"""

import csv
import string
from PIL import Image
import pytesseract

def ocr(img):
    pixdata = img.load()
    colors = {}
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if colors.has_key(pixdata[x, y]):
                colors[pixdata[x, y]] += 1
            else:
                colors[pixdata[x, y]] = 1
    colors = sorted(colors.items(), key=lambda d:d[1], reverse=True)
    significant = colors[1][0]
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if pixdata[x, y] != significant:
                pixdata[x, y] = (255, 255, 255)
            else:
                pixdata[x, y] = (0, 0, 0)
    img.save('076_bw.png')
    #需要将配置文件和图片复制到pytesseract源码路径下面
    word = pytesseract.image_to_string(img, lang='eng', config='076_ocr.conf')
    ascii_word = ''.join(c for c in word if c in string.letters).lower()
    return ascii_word

files = ('076_whgn.jpeg', '076_fwuo.png', '076_ke8m.png', '076_m3hn.png', '076_5enn.png',
         '076_54xe.jpeg','076_ea6d.jpeg','076_kwdg.jpeg','076_mkek.jpeg','076_nkng.jpeg',
         '076_w3lh.jpeg', '076_teew.png')

def test_samples():
    for picfile in files:
        img = Image.open(picfile)
        print '%s is recognized as %s' % (file, ocr(img))

test_samples()