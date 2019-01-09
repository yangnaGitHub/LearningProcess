# -*- coding: utf-8 -*-
"""
Created on Mon Feb 06 15:31:45 2017

@author: natasha1_Yang
"""
import numpy as np

class Node(object):
    def __init__(self, Data = None, Left = None, Right = None, Father = None):
        self.Data = Data
        self.Left = Left
        self.Right = Right
        self.Father = Father
#归并排序合并序列   
def mergearray(points, start, midden, end, dimvalue):    
    array1start = start
    array1end = midden
    array2start = midden + 1
    array2end = end
    temp = np.zeros((end - start + 1, points.shape[1]));
    #print array1start, array1end, array2start, array2end, temp.shape
    index = 0
    while (array1start <= array1end) and (array2start <= array2end):
        #print points.shape, points[array1start][dimvalue], points[array2start][dimvalue]
        if(points[array1start][dimvalue] <= points[array2start][dimvalue]):
            temp[index] = points[array1start]
            index += 1
            array1start += 1
        else:
            temp[index] = points[array2start]
            index += 1
            array2start += 1
        
    #print array1start, array1end, array2start, array2end, temp.shape
    while array1start <= array1end:
        temp[index] = points[array1start]
        index += 1
        array1start += 1
    while array2start <= array2end:
        temp[index] = points[array2start]
        index += 1
        array2start += 1
    for listindex in range(index):
        points[start + listindex] = temp[listindex]
#归并排序主循环
def MySort(points, start, end, dimvalue):
    if start < end:
        midden = int((start + end) / 2)
        MySort(points, start, midden, dimvalue)
        MySort(points, midden + 1, end, dimvalue)
        mergearray(points, start, midden, end, dimvalue)
#Get中间的点    
def GetNodeIndex(points, start, end, dimvalue):
    MySort(points, start, end - 1, dimvalue)
    #print points
    middle_item_num = len(points) / 2
    return middle_item_num  
#创建树节点的主循环
def CreateSingalNode(points, start, end, dimvalue):
    points = points[start:end]
    #结束条件
    #print "CreateSingalNode", points, start, end, points.shape
    if 0 == points.shape[0]:
        return
    if 1 == points.shape[0]:
        return Node(points[0])
    nodeindex = GetNodeIndex(points, 0, end - start, dimvalue)
    dimvalue = (dimvalue + 1) % points.shape[1]
    root = Node(points[nodeindex])
    #print "Root:", points[nodeindex]
    #Left
    #print "index:", start, nodeindex, end
    root.Left = CreateSingalNode(points, 0, nodeindex, dimvalue)
    if root.Left != None:
        root.Left.Father = root
        #print "Left:", root.Left.Data
    #Right
    root.Right = CreateSingalNode(points, nodeindex + 1, end - start, dimvalue)
    if root.Right != None:
        root.Right.Father = root
        #print "Right:", root.Right.Data
    return root
    
def CreateKdTree(points):
    start = 0
    end = points.shape[0]
    dimvalue = 0
    return CreateSingalNode(points, start, end, dimvalue)

#根左右    
def ListAllTreeData(root):
    if root == None:
        return
    print root.Data
    ListAllTreeData(root.Left)
    ListAllTreeData(root.Right)

if __name__ == "__main__":
    pointslist = [
                  [2, 3],
                  [5, 4],
                  [9, 6],
                  [4, 7],
                  [8, 1],
                  [7, 2]
                  ]
    points = np.array(pointslist)
    root = CreateKdTree(points)
    ListAllTreeData(root)