# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 14:52:57 2018

@author: natasha_yang

@e-mail: ityangna0402@163.com
"""

语音识别:同样的发音到底是哪个词组出现的P是最大的
文本生成:很多候选的句子,最有可能的句子是哪个
N-gram ==> 2-gram
P(我爱妈妈) = P(我|START) * P(爱|我) * P(妈|爱) * P(妈|妈)
 其中 ==> P(爱|我) = C(我爱)/C(我)
 缺点:没有足够的data能估计出准确的几率,就是有很多二元组的P是0
 怎么解决:smooth有6种基本平滑方法
 建立矩阵可以解决0的问题
Grid LSTM
tree LSTM ==> recursiveNN的单元变成LSTM

LSTM和GRU的区别:
GRU有RESET和UPDATE两个门,他的输出不做任何控制就直接输出到下一个CELL
LSTM有forget,input和output三个门,然后输出是output做处理之后输出到下一个CELL

分词:正向/逆向/双向最大匹配
句法和语义分析消歧
互信息/CRF
wordEmbedding + bi-lstm + CRF
捕捉局部相关性