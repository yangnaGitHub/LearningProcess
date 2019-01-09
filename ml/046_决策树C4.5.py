# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 15:46:37 2017

@author: natasha1_Yang
"""


#-*-coding:utf-8-*-
# LANG=en_US.UTF-8
# ID3 和 ID4 算法
# 文件名：ID3_ID4.py
#

import sys
import math
import copy

dict_all = {
        # 1: 青年；2：中年；3：老年
        '_age' : [
                1, 1, 1, 1, 1,
                2, 2, 2, 2, 2,
                3, 3, 3, 3, 3,
            ],

        # 0：无工作；1：有工作
        '_work' : [
                0, 0, 1, 1, 0,
                0, 0, 1, 0, 0,
                0, 0, 1, 1, 0,
            ],

        # 0：无房子；1：有房子
        '_house' : [
                0, 0, 0, 1, 0,
                0, 0, 1, 1, 1,
                1, 1, 0, 0, 0,
            ],

        # 1：信贷情况一般；2：好；3：非常好
        '_credit' : [
                1, 2, 2, 1, 1,
                1, 2, 2, 3, 3,
                3, 2, 2, 3, 1,
            ],
    }

# 0：未申请到贷款；1：申请到贷款
_type = [
        0, 0, 1, 1, 0,
        0, 0, 1, 1, 1,
        1, 1, 1, 1, 0,
    ]

# 二叉树结点
class BinaryTreeNode( object ):
    def __init__( self, name=None, data=None, left=None, right=None, father=None ):
        self.name = name
        self.data = data
        self.left = left
        self.right = left

# 二叉树遍历
class BTree(object):
    def __init__(self,root=0):
        self.root = root

    # 中序遍历
    def inOrder(self,treenode):
        if treenode is None:
            return

        self.inOrder(treenode.left)
        print treenode.name, treenode.data
        self.inOrder(treenode.right)


# 遍历类型，统计每个类型的数量，将其保存到字典中
# 如：对于 _type: 有9个类型1，6个类型0。
# 于是返回：{'1': 9.0, '0': 6.0}
# 参数：类型列表
def get_type_num( type_list ):
    type_dict = {}
    tmp_item = ''

    for item in type_list:
        item = str(item)
        if tmp_item != item:
            if item in type_dict.keys():
                type_dict[item] += 1.0
            else:
                type_dict[item] = 1.0
                tmp_item = item
        else:
            type_dict[item] += 1.0

    return type_dict


# 获得熵
# 参数：类型列表
def get_entropy( type_list ):
    entropy = 0.0
    len_type = len(type_list)
    type_dict = get_type_num( type_list )
    # 计算熵
    for key in type_dict.keys():
        tmp_num = type_dict[key] / len_type
        entropy = entropy - tmp_num * math.log(tmp_num, 2)

    return float('%.3f' % entropy)


# 获得条件熵
# 参数：特征列表，类型列表，序号列表
# 如：
#   第一轮时以 _house 为特征进行筛选(筛选使用ID3或ID4，不是在此函数中)，这是参数分别为：_house, _type, [0, 1, ..., 15]
#   第一轮结束后：左子树的特征序号列表为：[3, 7, 8, 9, 10, 11]，右子树的特征序号列表为：[0, 1, 2, 4, 5, 6, 12, 13, 14]
#   于是第二轮在对右子树以 _work 为特征进行筛选时传入参数：_house, _type, [0, 1, 2, 4, 5, 6, 12, 13, 14]
def get_conditional_entropy( value_list, type_list, num_list ):
    # 整理 value_list 以 num_list 为序号形成的新列表中的不同类别
    # value_dict = {特征名 : 包含的类别列表}
    # eg：对于 _work
    #   其“原始内容”和“以 num_list(即：[0, 1, 2, 4, 5, 6, 12, 13, 14]) 为序号形成的新列表为”分别如下：
    #   [0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0]
    #   [0, 0, 1,    0, 0, 0,                1, 1, 0]
    #   新列表有3个类型1和6个类型2，于是该函数返回：{'1': [1, 1, 1], '0': [0, 0, 0, 0, 0, 0]}
    def get_value_type():
        value_dict = {}
        tmp_type = ''
        tmp_item = ''

        for num in num_list:
            item = str( value_list[num] )
            if tmp_item != item:
                if item in value_dict.keys():
                    value_dict[item].append(type_list[num])
                else:
                    value_dict[item] = [type_list[num],]
                    tmp_item = item
            else:
                value_dict[item].append(type_list[num])

        return value_dict

    value_dict = get_value_type()
    conditional_entropy = 0
    for key in value_dict.keys():
        tmp_num = float( '%.3f' % (float(len(value_dict[key]))/len(value_list)) )
        conditional_entropy += float( '%.3f' % (tmp_num * get_entropy(value_dict[key])) )
    
    return conditional_entropy

# 获得信息增益
def get_information_gain( value_list, type_list, num_list ):#index 4 0-14
    return float( '%.3f' % (get_entropy( type_list ) - get_conditional_entropy( value_list, type_list, num_list )) )


# 获得信息增益比
def get_information_gain_ratio( value_list, type_list, num_list ):
    entropy = get_entropy( type_list )
    information_gain = entropy - get_conditional_entropy( value_list, type_list, num_list )
    return float( '%0.3f' % (information_gain/entropy) )


# ID3 算法
def ID3( data, type_list, threshold ):
    # 获得最大的信息增益
    def get_max_information_gain( num_list ):
        step = 'continue'
        tmp_value = 0.0
        feature_name = ''

        for key in data.keys():
            information_gain = get_information_gain( data[key], type_list, num_list )
            if information_gain > tmp_value:
                feature_name = key
            tmp_value = information_gain

        # 如果信息增益小于阈值，则告诉后面的程序，不用在迭代了，到此即可
        if information_gain < threshold:
            step = 'over'

        return feature_name, step

    # 进行分类
    def classify( root, note_name, note_data, note_type ):
        # 将'特征可能值名字'追加到 root.name 中
        # 将[样本序号的列表]合并到 root.data 中
        root.name.append( note_name )
        root.data.extend( note_data )#extend

        # note_type=='exit' 意味着当前的数据全部属于某一类，不用在分类了
        if not data or note_type=='exit':
            return

        feature_name, step = get_max_information_gain( note_data )

        # 根据特征的可能值将样本数据分成数个集合，并保存成“特征字典”。
        # 字典结构为：{ '特征可能值名字': [样本序号的列表] }
        feature_dict = {}
        tmp_item = ''
        for num in note_data:
            item = str( data[feature_name][num] )
            if tmp_item != item:
                if item in feature_dict.keys():
                    feature_dict[item].append(num)
                else:
                    feature_dict[item] = [num, ]
                    tmp_item = item
            else:
                feature_dict[item].append(num)

        # 从样本集合中将该特征删除
        del data[feature_name]

        # 准备左子节点和右子节点，节点的 name 和 data 是个空列表
        root.left = BinaryTreeNode( [], [] )
        root.right = BinaryTreeNode( [], [] )

        # 计算“特征字典”中各个集合中是属于“能贷贷款”的多还是“不能贷贷款”的多
        # 如果是前者：
        #   递归调用 classify，形成左子节点
        # 如果是后者：
        #   递归调用 classify，形成右子节点
        for key in feature_dict.keys():
            num_yes = 0; num_no = 0
            for num in feature_dict[key]:
                if type_list[num] == 1:
                    num_yes = num_yes + 1
                elif type_list[num] == 0:
                    num_no = num_no + 1
                else:
                    print 'ERROR: wrong type in _type'
                    exit()

            note_type = 'not_exit'
            if num_yes == 0 or num_no == 0 or step == 'over':
                note_type = 'exit'
            
            if num_yes >= num_no:
                classify( root.left, '%s:%s' % (feature_name, key), feature_dict[key], note_type )
            else:
                classify( root.right, '%s:%s' % (feature_name, key), feature_dict[key], note_type )
        
        return root


    tmp_list = []
    for num in xrange( len(dict_all[dict_all.keys()[0]]) ):
        tmp_list.append( num )
    return classify( BinaryTreeNode( [], [] ), 'root', tmp_list, 'not_exit' )


# C4.5 算法
def C4_5( data, type_list, threshold ):
    # 获得最大的信息增益比
    def get_max_information_gain( num_list ):
        step = 'continue'
        tmp_value = 0.0
        feature_name = ''

        for key in data.keys():
            information_gain_ratio = get_information_gain_ratio( data[key], type_list, num_list )
            if information_gain_ratio > tmp_value:
                feature_name = key
            tmp_value = information_gain_ratio

        # 如果信息增益比小于阈值，则告诉后面的程序，不用在迭代了，到此即可
        if information_gain_ratio < threshold:
            step = 'over'

        return feature_name, step

    # 进行分类
    def classify( root, note_name, note_data, note_type ):
        # 将'特征可能值名字'追加到 root.name 中
        # 将[样本序号的列表]合并到 root.data 中
        root.name.append( note_name )
        root.data.extend( note_data )

        # note_type=='exit' 意味着当前的数据全部属于某一类，不用在分类了
        if not data or note_type=='exit':
            return

        feature_name, step = get_max_information_gain( note_data )

        # 根据特征的可能值将样本数据分成数个集合，并保存成“特征字典”。
        # 字典结构为：{ '特征可能值名字': [样本序号的列表] }
        feature_dict = {}
        tmp_item = ''
        for num in note_data:
            item = str( data[feature_name][num] )
            if tmp_item != item:
                if item in feature_dict.keys():
                    feature_dict[item].append(num)
                else:
                    feature_dict[item] = [num, ]
                    tmp_item = item
            else:
                feature_dict[item].append(num)

        # 从样本集合中将该特征删除
        del data[feature_name]

        # 准备左子节点和右子节点，节点的 name 和 data 是个空列表
        root.left = BinaryTreeNode( [], [] )
        root.right = BinaryTreeNode( [], [] )

        # 计算“特征字典”中各个集合中是属于“能贷贷款”的多还是“不能贷贷款”的多
        # 如果是前者：
        #   递归调用 classify，形成左子节点
        # 如果是后者：
        #   递归调用 classify，形成右子节点
        for key in feature_dict.keys():
            num_yes = 0; num_no = 0
            for num in feature_dict[key]:
                if type_list[num] == 1:
                    num_yes = num_yes + 1
                elif type_list[num] == 0:
                    num_no = num_no + 1
                else:
                    print 'ERROR: wrong type in _type'
                    exit()

            note_type = 'not_exit'
            if num_yes == 0 or num_no == 0 or step == 'over':
                note_type = 'exit'
            
            if num_yes >= num_no:
                classify( root.left, '%s:%s' % (feature_name, key), feature_dict[key], note_type )
            else:
                classify( root.right, '%s:%s' % (feature_name, key), feature_dict[key], note_type )
        
        return root


    tmp_list = []
    for num in xrange( len(dict_all[dict_all.keys()[0]]) ):
        tmp_list.append( num )
    return classify( BinaryTreeNode( [], [] ), 'root', tmp_list, 'not_exit' )


# 阈值
threshold = 0.3
dict_all_id3 = copy.deepcopy( dict_all )
root = ID3( dict_all_id3, _type, threshold )
bt = BTree( root )
print '--------------ID3----------------'
bt.inOrder( bt.root )
print '---------------------------------\n'

dict_all_c45 = copy.deepcopy( dict_all )
root = C4_5( dict_all_c45, _type, threshold )
bt = BTree( root )
print '--------------C4.5----------------'
bt.inOrder( bt.root )
print '----------------------------------\n'

