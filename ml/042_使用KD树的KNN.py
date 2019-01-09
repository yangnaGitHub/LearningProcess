# -*- coding: utf-8 -*-
"""
Created on Mon Feb 06 15:27:44 2017

@author: natasha1_Yang
"""

import sys  
import math  
  
list_T = [  
    ( 2, 3 ),  
    ( 5, 4 ),  
    ( 9, 6 ),  
    ( 4, 7 ),  
    ( 8, 1 ),  
    ( 7, 2 ),  
        ]  
  
# 二叉树结点  
class BinaryTreeNode( object ):  
    def __init__( self, data=None, left=None, right=None, father=None ):  
        self.data = data  
        self.left = left  
        self.right = left  
        self.father = father  
  
# 二叉树遍历  
class BTree(object):  
    def __init__(self,root=0):  
        self.root = root  
  
    # 中序遍历  
    def inOrder(self,treenode):  
        if treenode is None:  
            return  
  
        self.inOrder(treenode.left)  
        print treenode.data  
        self.inOrder(treenode.right)  
          
  
# 快速排序算法  
# 1，取当前元素集的第一个元素为 key，i = 0，j = len(当前元素集)  
# 2，j-- 直到找到小于 key 的元素，然后 L[i] 与 L[j] 交换  
# 3，i++ 直到找到大于 key 的元素，然后 L[i] 与 L[j] 交换  
# 4，当 i == j 时停止  
# 5，L[i] = key  
# 此时当前元素集被第 i 个元素分成了左右两部分，左边的都比 key 小，右边的都比 key 大  
# 6，对左右两部分重复上面 5 步直到再无分割  
def quick_sort( T, left, right, rank):  
    tmp_i = left  
    tmp_j = right  
  
    if left >= right:  
        return  
  
    key = T[left][rank]; key_item = T[left]  
    while tmp_i != tmp_j:  
        while tmp_i < tmp_j and T[tmp_j][rank] > key:  
            tmp_j -= 1  
        T[tmp_i] = T[tmp_j]  
  
        while tmp_i < tmp_j and T[tmp_i][rank] < key:  
            tmp_i += 1  
        T[tmp_j] = T[tmp_i]  
  
    T[tmp_i] = key_item  
  
    quick_sort( T, left, tmp_i-1, rank )  
    quick_sort( T, tmp_i+1, right, rank )  
  
    return T  
  
  
# 制作 kd 树  
#   原队列： [(2, 3), (5, 4), (9, 6), (4, 7), (8, 1), (7, 2)]  
#   1，以x轴为基准排列  ： [(2, 3), (4, 7), (5, 4), (7, 2), (8, 1), (9, 6)]  
#   2，取中间的数为根，这时会产生左节点集和右节点集，即：经过(7, 2)的垂直于 x 轴的超平面 1 将整个矩形区域分成了左右两部分：  
#                                       (7, 2)  
#                                       /    \  
#                                      /      \  
#                                     /        \  
#               [(2, 3), (4, 7), (5, 4)]      [(8, 1), (9, 6)]  
#   3，对左右子树集以 x 轴为基准排列：  
#               [(2, 3), (5, 4), (4, 7)]      [(8, 1), (9, 6)]  
#   4，取中间的数为父节点，这时会产生左节点集和右节点集，即：经过 (5, 4) 和 (9, 6) 的垂直于超平面 1 (或者说 y 轴)的超平面将上面的两个左右区域又分成了两部分  
#                               (5, 4)         (9, 6)  
#                                /  \            /  
#                               /    \          /  
#                           (2, 3)  (4, 7)  (8, 1)  
#   循环上面 4 步，直到没有结点。  
#   最终 kd 树如下图所示：  
#                            (7, 2)  
#                            /    \  
#                           /      \  
#                      (5, 4)      (9, 6)  
#                       /  \         /  
#                      /    \       /  
#                  (2, 3)  (4, 7)  (8, 1)  
def make_kd_tree( T ):  
  
    # 获取中间的数   
    def get_middle_item( _input ):  
        middle_item_num = len( _input ) / 2  
        middle_item = _input[middle_item_num]  
  
        return middle_item, middle_item_num  
  
    # kd 树的迭代函数  
    #   参数：二叉树的结点，上一步的结点集，当前迭代时结点集的最小序号，最大序号，秩  
    def iter_for_kd_tree( root, tmp_T, left, right, rank ):  
        # 根据 left 和 right 截取 tmp_T，tmp_T 为上一步的结点集，如：  
        # 在第一次迭代后，若当前循环的是左结点集，那 left = 0，right = middle_item_num  
        # 于是本次就是在 [(2, 3), (5, 4), (4, 7)] 这个结点集中选择中位点并继续了。  
        tmp_T = tmp_T[left: right]  
  
        # 若当前的结点集中已无节点，就返回 None  
        if len(tmp_T) == 0: return  
  
        # 若当前结点中只有一个元素，那就创建并返回用该元素创建的二叉树结点  
        if len(tmp_T) == 1:  
            return BinaryTreeNode( tmp_T[0] )  
  
        # 对当前的结点集以当前的秩为基准进行排列  
        quick_sort( tmp_T, 0, len(tmp_T)-1, rank )  
        # 更新秩，为下次排列做准a  
        rank = (rank + 1) % len(T[0])  
        # 获取当前结点集的中间元素和中间元素的坐标(该坐标用于将当前结点集分离成两部分)  
        middle_item, middle_item_num = get_middle_item( tmp_T )  
        # 使用该中间元素创建一个二叉树结点  
        root = BinaryTreeNode( middle_item )  
        # 将 "root 的左子结点，当前的结点集，左边结点集的最小坐标，左边结点集的最大坐标，秩" 传入本函数进行迭代  
        # 返回的结点保存到 root 的左子结点  
        root.left = iter_for_kd_tree( root.left, tmp_T, 0, middle_item_num, rank )  
        # root 的左子结点的父结点指向 root 自己  
        if root.left != None: root.left.father = root  
        # 同上，保存到 root 的右子结点  
        root.right = iter_for_kd_tree( root.right, tmp_T, middle_item_num+1, len(tmp_T), rank )  
        if root.right != None: root.right.father = root  
        # 返回根  
        return root  
  
    rank = 0 # 第一次在 x 轴上找中位点  
    return iter_for_kd_tree( BinaryTreeNode(), T, 0, len(T), rank )  
  
  
# 使用 kd 树，进行 k 近邻算法  
def use_kd_tree( T, root, target ):  
  
    # 得到两点间的距离  
    def get_distance( x, y ):  
        distance = (x[0] - y[0]) * (x[0] - y[0]) + (x[1] - y[1]) * (x[1] - y[1])  
        return math.sqrt( distance )  
  
    # 中序遍历 kd 树，得到包含 target 的叶子结点  
    def inOrder( node, rank ):  
        # 如果该结点没有左子结点和右子结点，那该结点就是叶子结点了  
        if not node.left and not node.right:  
            return node  
  
        # 保存当前的秩  
        tmp_rank = rank  
        # 更新秩  
        rank = (rank + 1) % len(T[0])  
          
        # 从根结点出发，如果目标点在当前秩的坐标 < node 在当前秩的坐标  
        if target[tmp_rank] <= node.data[tmp_rank]:  
            # 移动到左子结点  
            node = inOrder( node.left, rank )  
        else:  
            # 反之移动到右子结点  
            node = inOrder( node.right, rank )  
              
        return node  
  
    # 得到最近的点  
    def find_close_node( node, target, close_node ):  
  
        # 遍历到根结点就 ok 了  
        if not node.father: return  
          
        # 计算当前最近邻点距离  
        min_distance = get_distance( node.data, target )  
        # 计算 target 距离当前最邻近点的父节点的距离  
        new_distance = get_distance( node.father.data, target )  
  
        # 如果距离父节点更近  
        if min_distance >= new_distance:  
            min_distance = new_distance  
            # 将父节点保存成“当前最近邻点”  
            close_node = node.father.data  
  
            # 判断父节点的另外一个结点距离 target 是否更近，记得话将其保存成“当前最近邻点”  
            if node.father.left != node:  
                new_distance = get_distance( node.father.left.data, target )  
                if min_distance >= new_distance:  
                    close_node = node.father.left.data  
            else:  
                new_distance = get_distance( node.father.right.data, target )  
                if min_distance >= new_distance:  
                    close_node = node.father.right.data  
  
        find_close_node( node.father, target, close_node )  
        return close_node  
  
    rank = 0  
    node = inOrder( root, rank )  
    close_node = node.data  
    find_close_node( node, target, close_node )  
    return close_node  
  
  
root = make_kd_tree( list_T )  
  
target = (3, 6)  
print use_kd_tree( list_T, root, target )  