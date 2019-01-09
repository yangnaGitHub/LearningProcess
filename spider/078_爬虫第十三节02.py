# -*- coding: utf-8 -*-
"""
Created on Thu Aug 03 17:28:34 2017

@author: natasha1_Yang
"""

import scipy as sp  
import numpy as np  
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import SGDClassifier
from sklearn.datasets import load_files  
from sklearn.model_selection import train_test_split  
from sklearn.feature_extraction.text import  TfidfVectorizer  
from sklearn.feature_extraction.text import  TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
from sklearn.naive_bayes import MultinomialNB
import jieba

movie_reviews = load_files('078_comment')#load目录中文件的数据

f = open('078_stopwords.txt', 'rb')
stop_words_raw = f.read()
f.close()

stop_words = stop_words_raw.split('\n')

# BOOL型特征下的向量空间模型
count_vec = CountVectorizer(binary = False, decode_error = 'ignore', tokenizer=jieba.cut, stop_words=stop_words)  
x_train_vec = count_vec.fit_transform(movie_reviews.data)

tfidf_transformer = TfidfTransformer()
x_train_tfidf = tfidf_transformer.fit_transform(x_train_vec)

lr = LogisticRegression()
lr.fit(x_train_tfidf, movie_reviews.target)

clf = MultinomialNB().fit(x_train_tfidf, movie_reviews.target)

ratings_new = ['电影很好看','不好看','很不错的电影，太棒了','太赞了，很值得看的电影','烂','好让我失望']
x_new_counts = count_vec.transform(ratings_new)
x_new_tfidf = tfidf_transformer.transform(x_new_counts)
print lr.predict(x_new_tfidf)
print clf.predict(x_new_tfidf)

kmeans = KMeans(2).fit(x_train_tfidf)
labels = kmeans.predict(x_train_tfidf)
print labels
print movie_reviews.target

doc_terms_train, doc_terms_test, y_train, y_test = train_test_split(movie_reviews.data, movie_reviews.target, test_size = 0.3)  
x_train = count_vec.fit_transform(doc_terms_train)
x_test = count_vec.transform(doc_terms_test)
x = count_vec.transform(movie_reviews.data)
y = movie_reviews.target

print count_vec.get_feature_names()
print x_train.toarray()
