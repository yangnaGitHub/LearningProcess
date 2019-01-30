# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 16:06:19 2019

@author: natasha_yang

@e-mail: ityangna0402@163.com
"""

import pandas as pd
import numpy as np

#索引在左边,值在右边
x_data = pd.Series([1, 3, 6, np.nan, 44, 1])
print(x_data)

#表格型的数据结构
dates = pd.date_range('20180101', periods=6)
df = pd.DataFrame(np.random.randn(6,4), index=dates, columns=['a', 'b', 'c', 'd'])
print(df)
print(df['b'])#列
print(df.b)#列
print(df[0:3])#行
print(df['20180101':'20180102'])#行
#loc是列的名称
print(df.loc['20180103'])#行
print(df.loc[:, ['a', 'b']])#列
print(df.loc['20180103', ['a', 'b']])
#是index
print(df.iloc[3, 1])#0,0开始
print(df.iloc[3:5, 1:3])
print(df.iloc[[1, 3, 5], 1:3])
#是列名称和index的组合
#print(df.ix[:3, ['a', 'c']])
print(df[df.a>0.5])
df['e'] = pd.Series([1, 2, 3, 4, 5, 6], index=pd.date_range('20180101', periods=6)) 
print(df)

#pd.dropna()直接去掉有NaN的行或列
#pd.fillna()将NaN的值用其他值代替
#pd.isnull()判断是否有缺失数据NaN

df1 = pd.DataFrame(np.ones((3,4))*0, columns=['a', 'b', 'c', 'd'])
df2 = pd.DataFrame(np.ones((3,4))*1, columns=['a', 'b', 'c', 'd'])
df3 = pd.DataFrame(np.ones((3,4))*2, columns=['a', 'b', 'c', 'd'])
res = pd.concat([df1, df2, df3], axis=0)#纵向
print(res)
#ignore_index重置index
res = pd.concat([df1, df2, df3], axis=0, ignore_index=True)
print(res)
#join合并方式
df1 = pd.DataFrame(np.ones((3,4))*0, columns=['a', 'b', 'c', 'd'], index=[1,2,3])
df2 = pd.DataFrame(np.ones((3,4))*1, columns=['b', 'c', 'd', 'e'], index=[2,3,4])
#纵向外合并df1与df2,有相同的column上下合并在一起,其他独自的column个自成列,原本没有值的位置皆以NaN填充
res = pd.concat([df1, df2], axis=0, join='outer')
print(res)

res = pd.concat([df1, df2], axis=0, join='inner')
print(res)

#join_axes依照axes合并
df1 = pd.DataFrame(np.ones((3,4))*0, columns=['a', 'b', 'c', 'd'], index=[1,2,3])
df2 = pd.DataFrame(np.ones((3,4))*1, columns=['a', 'b', 'c', 'd'], index=[2,3,4])
res = pd.concat([df1, df2], axis=1, join_axes=[df1.index])
print(res)

res = pd.concat([df1, df2], axis=1, join_axes=[df2.index])
print(res)

res = pd.concat([df1, df2], axis=1)
print(res)

#append只有纵向合并,没有横向合并
df1 = pd.DataFrame(np.ones((3,4))*0, columns=['a', 'b', 'c', 'd'])
df2 = pd.DataFrame(np.ones((3,4))*1, columns=['a', 'b', 'c', 'd'])
df3 = pd.DataFrame(np.ones((3,4))*1, columns=['a', 'b', 'c', 'd'])
s1 = pd.Series([1, 2, 3, 4], index=['a', 'b', 'c', 'd'])

res = df1.append(df2, ignore_index=True)
print(res)

res = df1.append([df2, df3], ignore_index=True)
print(res)

res = df1.append(s1, ignore_index=True)
print(res)

left = pd.DataFrame({'key': ['K0', 'K1', 'K2', 'K3'],
                     'A': ['A0', 'A1', 'A2', 'A3'],
                     'B': ['B0', 'B1', 'B2', 'B3']})
right = pd.DataFrame({'key': ['K0', 'K1', 'K2', 'K3'],
                      'C': ['C0', 'C1', 'C2', 'C3'],
                      'D': ['D0', 'D1', 'D2', 'D3']})
print(left)
print(right)
#依据key column合并
res = pd.merge(left, right, on='key')
print(res)

left = pd.DataFrame({'key1': ['K0', 'K0', 'K1', 'K2'],
                     'key2': ['K0', 'K1', 'K0', 'K1'],
                     'A': ['A0', 'A1', 'A2', 'A3'],
                     'B': ['B0', 'B1', 'B2', 'B3']})
right = pd.DataFrame({'key1': ['K0', 'K1', 'K1', 'K2'],
                      'key2': ['K0', 'K0', 'K0', 'K0'],
                      'C': ['C0', 'C1', 'C2', 'C3'],
                      'D': ['D0', 'D1', 'D2', 'D3']})
res = pd.merge(left, right, on=['key1', 'key2'], how='inner')
print(res)

res = pd.merge(left, right, on=['key1', 'key2'], how='outer')
print(res)

res = pd.merge(left, right, on=['key1', 'key2'], how='left')
print(res)

res = pd.merge(left, right, on=['key1', 'key2'], how='right')
print(res)

#indicator=True会将合并的记录放在新的一列
df1 = pd.DataFrame({'col1':[0, 1], 'col_left':['a', 'b']})
df2 = pd.DataFrame({'col1':[1, 2, 2],'col_right':[2, 2, 2]})
res = pd.merge(df1, df2, on='col1', how='outer', indicator=True)
print(res)

res = pd.merge(df1, df2, on='col1', how='outer', indicator='indicator_column')
print(res)

res = pd.merge(left, right, left_index=True, right_index=True, how='outer')
print(res)

res = pd.merge(left, right, left_index=True, right_index=True, how='inner')
print(res)

boys = pd.DataFrame({'k': ['K0', 'K1', 'K2'], 'age': [1, 2, 3]})
girls = pd.DataFrame({'k': ['K0', 'K0', 'K3'], 'age': [4, 5, 6]})
res = pd.merge(boys, girls, on='k', suffixes=['_boy', '_girl'], how='inner')
print(res)