# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 16:59:10 2017

@author: natasha1_Yang
"""

#CART算法
#1>决策树生成:基于训练数据集生成决策树,生成的决策树要尽量大
#2>决策树剪枝:用验证数据集对已生成的树进行剪枝并选择最优子树,这是用损失函数最小作为剪枝的标准
#决策树额度生成就是递归构建二叉决策树的过程
#    回归树:平方误差最小化标准特征选择
#    分类树:基尼系数最小化标准特征选择,Gini系数代表了不确定性,越大越不确定
#基尼指数:
#    N各类,样本点属于第K个类的概率为Pk ==> Pk(1-Pk) k=(1,...,N)的加和
#针对045的数据计算:D是样本集合,data[0]==>A0以此类推
#    求A0的Gini系数:Gini(D, A1 = 0) = |D0|/|D|Gini(D0) + |D1|/|D|Gini(D1)==>D0:青年, D1不是青年
#        二分类问题,所以A1 = 0或是A1 != 0,使用前面的公式Gini(P) = 2P(1 - P),P是贷到款
#        = (5/15)Gini(D0) + (10/15)Gini(D1)
#        = (1/3)(2 * (2/5) * (1 - (2/5))) + (2/3)(2 * (7/10) * (1 - (7/10)))
#        同理求Gini(D, A1 = 1)和Gini(D, A1 = 2)
#        在这些Gini指数中选择最小的来做切分点
#    同理计算A1和A2以及A3的所有的Gini系数
#    在所有的选择最小的Gini系数来作为最优的切分点和最优的特征
#    重复此过程选择下一个特征和最优的切分点
#    结束条件:使用预定阈值 + 特征全被使用/样本数据被完全分类
#CART剪枝:REP + PEP + REP + CPP + MEP + MECM + MPL
#代价-复杂度剪枝CPP:使用误差增益值作为判断标准
#对于任意内部节点:g(t) = (R(t) - R(Tt)) / Qc
#    Qc = |叶子节点的个数| - 1
#    R(t):节点的误差代价(如果该节点被剪枝的话) = r(t) * P(t)
#        r(t):某节点上有x个属于目标类,y个不属于 = y/(x+y)
#        P(t):某节点上有x个元素,所有节点共有y个元素 = x/y
#    R(Tt):子树的误差代价
#        节点不被剪枝 = 子树上所有叶子节点的误差代价之和
#    递归求出所有非叶子节点的g(t)
#    找到最小的那个非叶子节点剪枝掉(变成叶子节点)
#    PS:当有多个非叶子节点同时最小的时候,取Qc最大的进行剪枝
#决策树有60个元素,非叶子节点如下图,求其不属于类1的误差增益值
#            T4(9, 7)
#        T6(3, 4)    T7(6, 3):类1
# 类1:T8(3, 2)  T9(0 2):类2
#说明:T7中6个元素属于类1,3个不属于,以此类推其他的叶子节点
#对于节点T4:R(t) = r(t) * P(t) = (7/(9+7)) * ((9+7)/60)
#    Qc = 3个叶子节点 = 3 - 1 = 2
#    R(Tt) = 叶子节点误差代价之和 = R(T7) + R(T8) + R(T9)
#        = (3/9)*(9/60) + (2/5)*(5/60) + (2/2)(2/60)
import numpy as np
import copy

class TreeNode(object):
    def __init__(self, name = None, data = None, left = None, right = None, father = None, number = 1):
        self.name = name
        self.data = data
        self.left = left
        self.right = right
        self.father = father
        self.number = number
    
    def InOrder(self, node, No):
        if node is None:
            return
        node.number = No
        #print node.name, node.data, node.number
        self.InOrder(node.left, 2 * node.number)
        self.InOrder(node.right, 2 * node.number + 1)
        
def CalcClassfierGini(data_value):
    data = [money[1] for money in data_value]
    count = len(data)
    value_list = list(set(data))
    value_pro = np.zeros(len(value_list))
    for mindex in range(len(value_list)):
        for nindex in range(count):
            if value_list[mindex] == data[nindex]:
                value_pro[mindex] += 1
        #print "value_pro", value_pro[mindex]
    for mindex in range(len(value_list)):
        value_pro[mindex] = float(value_pro[mindex]) / float(count)
        value_pro[mindex] = value_pro[mindex] * (1 - value_pro[mindex])
    return sum(value_pro)
    
def CalcFeatureGiniMin(data_dict, Filter_Feature_List):
    Key = "money"
    Index = 0
    MinGini = float("inf")
    IndexCount = 0
    for key in data_dict.keys():
        if key not in Filter_Feature_List:
            data = data_dict[key]
            count = len(data_dict[key])
            value_list = list(set(data))
            data_count = np.zeros(len(value_list))
            data_value = np.zeros(len(value_list), dtype = float)
            #print data
            for index in range(len(value_list)):
                for items in data:
                    if value_list[index] == items:
                        data_count[index] += 1
            for index in range(len(value_list)):
                temp_data = np.zeros(((int)(data_count[index]), 2))
                temp_data_res = np.zeros(((int)(count - data_count[index]), 2))
                mindex = 0
                nindex = 0
                for items in range(count):
                    if value_list[index] == data[items]:
                        temp_data[mindex][0] = data[items]
                        temp_data[mindex][1] = data_dict["money"][items]
                        mindex += 1
                    else:
                        temp_data_res[nindex][0] = data[items]
                        temp_data_res[nindex][1] = data_dict["money"][items]
                        nindex += 1
                pro_value = float(data_count[index])/float(count)
                data_value[index] = pro_value*CalcClassfierGini(temp_data) + (1 - pro_value)*CalcClassfierGini(temp_data_res)
                if MinGini > data_value[index]:
                    MinGini = data_value[index]
                    Key = key
                    Index = value_list[index]
                    IndexCount = data_count[index]
                #print key, value_list[index], data_value[index]
    return Key, Index, IndexCount
    
def CreateDecisionTree(name, data, Filter_Feature_List):
    if 1 == len(set(data["money"])):
        child = TreeNode()
        child.name = name
        child.data = data
        return child
    Key, Index, IndexCount = CalcFeatureGiniMin(data, Filter_Feature_List)
    root = TreeNode()
    root.name = Key
    root.data = data
    #print "Key", Key, Index
    Filter_Feature_List.append(Key)
    data_dict_left = {}
    data_dict_right = {}
    for index in range(len(data[Key])):
        if Index == data[Key][index]:
            for key in data.keys():
                if key in data_dict_left.keys():
                    data_dict_left[key].append(data[key][index])
                else:
                    data_dict_left[key] = [data[key][index],]
        else:
            for key in data.keys():
                if key in data_dict_right.keys():
                    data_dict_right[key].append(data[key][index])
                else:
                    data_dict_right[key] = [data[key][index],]
    #print data_dict_left
    #print data_dict_right
    root.left = CreateDecisionTree(Key, data_dict_left, Filter_Feature_List)
    if root.left != None:
        root.left.father = root
    root.right = CreateDecisionTree(Key, data_dict_right, Filter_Feature_List)
    if root.right != None:
        root.right.father = root
    return root

Qcount = [0]
def CalcLeafNodeCount(node):
    if node is None:
        return
    Qcount[0] += 1
    CalcLeafNodeCount(node.left)
    CalcLeafNodeCount(node.right)

#总共15个样本
#rt * pt 分错/节点样本总数 * 节点个数/总共样本
def CalcRt(node):
    
#计算所有叶子节点的Rt  
def CalcRTt(node):
    
    
#任意内部节点
MinGt = [int(0), float("inf")]
def CalcGt(node):
    if node.left is None:
        if node.right is None:
            return 
    CalcLeafNodeCount(node)
    Qc = Qcount[0] - 1
    Qcount[0] = 0
    Rt = CalcRt(node)
    RTt = CalcRTt(node)
    Gt = (float)(Rt - RTt)/(float)Qc
    if MinGt[1] > Gt:
        MinGt[1] = Gt
        MinGt[0] = node.number
    CalcGt(node.left)
    CalcGt(node.right)

def RemoveBranch(node):
    CalcGt(node)
    
if __name__ == "__main__":
    data = np.loadtxt("045_DTDATA.csv", dtype = int, delimiter = ',', usecols = (range(1, 6)))
    #转成Dictionary的数据格式
    data_dict = {}#字典无序
    data_dict["age"] = [col[0] for col in data]
    data_dict["work"] = [col[1] for col in data]
    data_dict["house"] = [col[2] for col in data]
    data_dict["credit"] = [col[3] for col in data]
    data_dict["money"] = [col[4] for col in data]
    data_dict_copy = copy.deepcopy(data_dict)
    Filter_Feature_List = ["money"]
    root = CreateDecisionTree("money", data_dict_copy, Filter_Feature_List)
    root.InOrder(root, 1)
    #剪枝
    RemoveBranch(root)