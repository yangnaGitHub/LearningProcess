# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 16:33:54 2016

@author: natasha1_Yang
"""

#eval()
import sys,os
from opencv.cv import *
from opencv.highgui import *
from PIL import Image,ImageDraw
from math import sqrt

def detectObjects(image):
    grayscale = cvCreateImage(cvSize(image.width, image.height), 8, 1)
    cvCvtColor(image, grayscale, CV_BGR2GRAY)
    
    storage = cvCreateMemStorage(0)
    cvClearMemStorage(storage)
    cvEqualizeHist(grayscale, grayscale)
    
    cascade = cvLoadHaarClassifierCascade('''PATH''', cvSize(1, 1))
    face = cvHaarDetectObjects(grayscale, cascade, storage, 1.1, 2, CV_HAAR_DO_CANNY_PRUNING, cvSize(20, 20))
    
    result = []
    for f in faces:
        result.append((f.x, f.y, f.x + f.width, f.y + f.height))
    return result
    
def grayscale(r, g, b):
    return int(r*.3 + g*.59 + b*.11)
    
def process(infile, outfile):
    image = cvLoadImage(infile)
    if image:
        faces = detectObjects(image)
    im = Image.open(infile)
    if faces:
        draw = ImageDraw.Draw(im)
        for f in faces:
            draw.rectangle(f, outfile = (255, 0, 255))
        im.save(outfile, "JPEG", quality = 100)
    else:
        print "Error:cannot detect faces on %s" % infile

if __name__ == "__main__":
    process('''InfilePath, OutfilePath''')
    