# -*- coding: utf-8 -*-
"""
Created on Wed May 24 14:38:43 2017

@author: natasha1_Yang
"""

from PIL import Image
import sys

def decoder(im, threshold=200, mask="076_letters.bmp", alphabet="0123456789abcdef"):
    img = Image.open(im)
    img = img.convert("RGB")
    box = (8, 8, 58, 18)#起始点的横坐标,起始点的纵坐标,宽度,高度
    img = img.crop(box)
    pixdata = img.load()
    
    letters = Image.open(mask)
    ledata = letters.load()
    
    def test_letter(img, letter):
        A = img.load()
        B = letter.load()
        mx = 1000000
        max_x = 0
        x = 0
        print img.size[0], letter.size[0], img.size[0] - letter.size[0]
        for x in range(img.size[0] - letter.size[0]):
            _sum = 0
            for i in range(letter.size[0]):
                for j in range(letter.size[1]):
                    _sum = _sum + abs(A[x + i, j][0] - B[i, j][0])
            if _sum < mx:
                mx = _sum
                max_x = x
        return mx, max_x
    
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if (pixdata[x, y][0] > threshold) and (pixdata[x, y][1] > threshold) and (pixdata[x, y][2] > threshold):
                pixdata[x, y] = (255, 255, 255, 255)
            else:
                pixdata[x, y] = (0, 0, 0, 255)
    
    counter = 0
    old_x = -1
    letterlist = []
    for x in range(letters.size[0]):
        black = True
        for y in range(letters.size[1]):
            if ledata[x, y][0] != 0:
                black = False
                break
        if black:
            box = (old_x + 1, 0, x, 10)
            letter = letters.crop(box)
            t = test_letter(img, letter)
            letterlist.append((t[0], alphabet[counter], t[1]))
            old_x = x
            counter += 1
    
    box = (old_x, 0, 140, 10)
    letter = letters.crop(box)
    t = test_letter(img, letter)
    letterlist.append((t[0], alphabet[counter], t[1]))
    
    t = sorted(letterlist)
    t = t[0:5]

    final = sorted(t, key=lambda e: e[2])
    
    answer = ''.join(map(lambda l: l[1], final))
    return answer

if __name__ == "__main__":
    print(decoder("076_test.jpg"))