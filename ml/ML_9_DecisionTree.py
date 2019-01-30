# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 10:55:17 2016

@author: natasha1_Yang
"""

class TreeNode:
    def __init__(self):
        self.sample = [] #该节点拥有哪些样本
        self.feature = -1 #使用第几号特征
        self.value = 0 #该特征的取值
        self.type = -1 #该节点的类型
        self.left = -1 #该节点的左孩子
        self.right = -1 #该节点的右孩子
        self.gini = 0 #Gini系数
        
    def gini_coefficient(self):
        types = {}
        for index in self.sample:
            singaltype = data[index][-1]
            if types.has_key(singaltype):
                types[singaltype] += 1
            else:
                types[singaltype] = 1
        pp = 0
        m = float(len(self.sample))
        for t in types:
            pp += (float(types[t]) / m) ** 2
        self.gini = 1 - pp
        max_type = 0
        for t in types:
            if max_type < types[t]:
                max_type = types[t]
                self.type = t

    def select_feature(self):
        n = len(data[0])
        if rf:
            return random.randint(0, n-2)
        gini_f = 1
        f = -1
        for index in range(n-1):
            g = self.gini_feature(index)
            if gini_f > g:
                gini_f = g
                f = index
        return f

    def choose_value(self, f, tree):
        f_max = self.calc_max(f)
        f_min = self.calc_min(f)
        step = (f_max - f_min) / granularity
        if step == 0:
            return f_min
        x_split = 0
        g_split = 1
        for x in numpy.arange(f_min+step, f_max, step):
            if rf:
                x = random.uniform(f_min, f_max)
            g = self.gini_coefficient2(f, x)
            if g_split > g:
                g_split = g
                x_split = x
        if g_split < self.gini: #分割后的gini系数要变小才有意义
            self.value = x_split
            self.feature = f
            t = TreeNode()
            t.sample = self.choose_sample(f, x_split, True)
            t.gini_coefficient()
            self.left = len(tree)
            tree.appeng(t)
            t = TreeNode()
            t.sample = self.choose_sample(f, x_split, False)
            t.gini_coefficient()
            self.right = len(tree)
            tree.appeng(t)
            
    def split(self, tree):
        f = self.select_feature()
        self.choose_value(f, tree)

def decision_tree():
    m = len(data)
    n = len(data[0])
    tree = []
    root = TreeNode()
    if rf:
        root.sample = random_select(alpha)
    else:
        root.sample = [x for x in range(m)]
    root.gini_coefficient()
    tree.append(root)
    first = 0
    last = 1
    for level in range(max_level):
        for node in range(first, last):
            tree[node].split(tree)
        first = last
        print level+1, len(tree)
    return tree

def predict_tree(d, tree):
    node = tree[0]
    while node.left != -1 and node.right != -1:
        if d[node.feature] < node.value:
            node = tree[node.left]
        else:
            node = tree[node.right]
    return node.type

def predict(d, forest):
    pd = {}
    for tree in forest:
        temp = predict_tree(d, tree)
        if pd.has_key(temp):
            pd[temp] += 1
        else:
            pd[temp] = 1
    number = 0
    temp = 0.0
    for p in pd:
        if number < pd[p]:
            number = pd[p]
