# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 11:24:42 2016

@author: natasha1_Yang
"""

#数据和特征决定了机器学习的上限,而模型和算法只是逼近这个上限而已
#特征工程:最大限度地从原始数据中提取特征以供算法和模型使用
############################
#使用sklearn中的preproccessing库
#不属于同一量纲==>无量纲化
#无量纲化方法有标准化和区间缩放法
#标准化的前提是特征值服从正态分布StandardScaler().fit_transform(iris.data)
#区间缩放法利用了边界值信息,将特征的取值区间缩放到某个特点的范围MinMaxScaler().fit_transform(iris.data)
#无量纲化是依照特征矩阵的列处理数据,正则化是依照特征矩阵的行处理数据
#正则化的前提是样本各特征值服从正态分布,样本均值和样本标准差改为特征值均值和特征值标准差Normalizer().fit_transform(iris.data)

#信息冗余
#定量特征二值化Binarizer(threshold=3).fit_transform(iris.data)

#定性特征不能直接使用,用哑编码的方式将定性特征转换为定量特征
#OneHotEncoder().fit_transform(iris.target.reshape((-1,1)))

#存在缺失值
#Imputer().fit_transform(vstack((array([nan, nan, nan, nan]), iris.data)))
#缺失值计算,返回值为计算缺失值后的数据
#参数missing_value为缺失值的表示形式,默认为NaN
#参数strategy为缺失值填充方式,默认为mean（均值）

#数据变换
#PolynomialFeatures().fit_transform(iris.data)#参数degree为度,默认值为2
#FunctionTransformer(log1p).fit_transform(iris.data)#自定义转换函数为对数函数的数据变换
#################################

################################
#特征选择==>feature_selection库来进行特征选择
#特征是否发散:一个特征不发散,例如方差接近于0,也就是说样本在这个特征上基本上没有差异,这个特征对于样本的区分并没有什么用
#特征与目标的相关性:这点比较显见,与目标相关性高的特征,应当优选选择
#Filter:按照发散性或者相关性对各个特征进行评分设定阈值或者待选择阈值的个数
#方差选择法:计算各个特征的方差根据阈值选择方差大于阈值的特征VarianceThreshold(threshold=3).fit_transform(iris.data)参数threshold为方差的阈值
#相关系数法:计算各个特征对目标值的相关系数以及相关系数的P值
#SelectKBest(lambda X, Y: array(map(lambda x:pearsonr(x, Y), X.T)).T, k=2).fit_transform(iris.data, iris.target)
#选择K个最好的特征,返回选择特征后的数据
#第一个参数为计算评估特征是否好的函数,该函数输入特征矩阵和目标向量,输出二元组的数组,数组第i项为第i个特征的评分和P值。在此定义为计算相关系数
#参数k为选择的特征个数
#卡方检验:检验定性自变量对定性因变量的相关性SelectKBest(chi2, k=2).fit_transform(iris.data, iris.target)
#互信息:是评价定性自变量对定性因变量的相关性的
#SelectKBest(lambda X, Y: array(map(lambda x:mic(x, Y), X.T)).T, k=2).fit_transform(iris.data, iris.target)
#
#Wrapper:根据目标函数每次选择若干特征或者排除若干特征
#递归特征消除法:使用一个基模型来进行多轮训练,每轮训练后消除若干权值系数的特征,再基于新的特征集进行下一轮训练
#RFE(estimator=LogisticRegression(), n_features_to_select=2).fit_transform(iris.data, iris.target)
#参数estimator为基模型,参数n_features_to_select为选择的特征个数
#
#Embedded:算法和模型进行训练得到各个特征的权值系数根据系数从大到小选择特征
#基于惩罚项的特征选择法:
#SelectFromModel(LogisticRegression(penalty="l1", C=0.1)).fit_transform(iris.data, iris.target)带L1惩罚项的逻辑回归作为基模型的特征选择
#树模型的特征选择法:SelectFromModel(GradientBoostingClassifier()).fit_transform(iris.data, iris.target)GBDT作为基模型的特征选择
#######################################

######################################
#降维
#主成分分析法（PCA）和线性判别分析（LDA）
#PCA(n_components=2).fit_transform(iris.data)参数n_components为主成分数目
#LDA(n_components=2).fit_transform(iris.data, iris.target)参数n_components为降维后的维数
#
#

























