# -*- coding: utf-8 -*-
"""
Created on Thu Aug 03 16:59:11 2017

@author: natasha1_Yang
"""

import scipy as sp
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import SGDClassifier
from sklearn.datasets import load_files
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
import jieba

movie_reviews = load_files('078_comment')#load目录中文件的数据

f = open('078_stopwords.txt', 'rb')
stop_words_raw = f.read()
f.close()

stop_words = stop_words_raw.split('\n')

#one-hot vector
count_vec = CountVectorizer(binary=False, decode_error='ignore', tokenizer=jieba.cut, stop_words=stop_words)
x_train_vec = count_vec.fit_transform(movie_reviews.data)

tfidf_transformer = TfidfTransformer()
x_train_tfidf = tfidf_transformer.fit_transform(x_train_vec)

linear_svc = SVC(kernel='linear')
rbf_svc = SVC(kernel='rbf')
sigmoid_svc = SVC(kernel='sigmoid')
poly_svc = SVC(kernel='poly')

linear_svc.fit(x_train_tfidf, movie_reviews.target)
rbf_svc.fit(x_train_tfidf, movie_reviews.target)
sigmoid_svc.fit(x_train_tfidf, movie_reviews.target)
poly_svc.fit(x_train_tfidf, movie_reviews.target)

ratings_new = ['电影很好看','不好看','很不错的电影，太棒了','太赞了，很值得看的电影','烂','好让我失望']
x_new_counts = count_vec.transform(ratings_new)
x_new_tfidf = tfidf_transformer.transform(x_new_counts)

print linear_svc.predict(x_new_tfidf)
print rbf_svc.predict(x_new_tfidf)
print sigmoid_svc.predict(x_new_tfidf)
print poly_svc.predict(x_new_tfidf)