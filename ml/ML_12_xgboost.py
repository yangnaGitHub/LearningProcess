#/usr/bin/python
#_*_ encoding:utf-8 _*_

import xgboost as xgb
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
import pandas ad pd
import csv
import os

def show_sccuracy(hat, test, tip):
    acc = hat.ravel() == test.ravel()
    acc_rate = 100 * float(acc.sum()) / hat.size
    retrun acc_rate

def load_data(file_name, is_train):
    data = pd.read_csv(file_name)
    data['Sex'] = data['Sex'].map({'female':0, 'male':1}).astype(int)

    if len(data.Fare[data.Fare.isnull()]) > 0:
        fare = np.zeros(3)
        for f in range(0, 3):
            fare[f] = data[data.Pclass == f+1]['Fare'].dropna().median()
        for f in range(0, 3):
            data.loc[(data.Fare.isnull()) & (data.Pclass == f+1), 'Fare'] = fare[f]

    if is_train:
        data_for_age = data[['Age', 'Survived', 'Fare', 'Parch', 'SibSp', 'Pclass']]
        age_exist = data_for_age.loc[(data.Age.notnull())]
        age_null = data_for_age.loc[(data.Age.isnull())]
        x = age_exist.values[:, 1:]
        y = age_exist.values[:, 0]
        rfr = RandomForestRegressor(n_estimators=1000)
        rfr.fit(x, y)
        age_hat = rfr.predict(age_null.values[:, 1:])
        data.loc[(data.Age.isnull()), 'Age'] = age_hat
    else:
        data_for_age = data[['Age', 'Fare', 'Parch', 'SibSp', 'Pclass']]
        age_exist = data_for_age.loc[(data.Age.notnull())]
        age_null = data_for_age.loc[(data.Age.isnull())]
        x = age_exist.values[:, 1:]
        y = age_exist.values[:, 0]
        rfr = RandomForestRegressor(n_estimators=1000)
        rfr.fit(x, y)
        age_hat = rfr.predict(age_null.values[:, 1:])
        data.loc[(data.Age.isnull()), 'Age'] = age_hat

    data.loc[(data.Embarked.isnull()), 'Embarked'] = 'S'
    embarked_data = pd.get_dummies(data.Embarked)
    embarked_data = embarked_data.rename(columns=lambda x: 'Embarked_' + str(x))
    data = pd.concat([data, embarked_data], axis=1)
    data.to_csv('New_Data.csv')

    x = data[['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked_C', 'Embarked_Q', 'Embarked_S']]
    y = None
    if 'Survived' in data:
        y = data['Survived']
    x = np.array(x)
    y = np.array(y)

    x = np.tile(x, (5, 1))
    y = np.tile(y, (5, ))
    if is_train:
        return x, y
    return x, data['PassengerId']
    

if __name__ == "__main__":
    os.chdir("E:\\MyOwner\\MyDocument\\ML_ChinaHadhoop\\12.XGBoost")
    x, y = load_data('12.Titanic.train.csv', True)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.5, random_state=1)

    lr = LogisticRegression(penalty='l2')
    lr.fit(x_train, y_train)
    y_hat = lr.predict(x_test)
    lr_rate = show_accuracy(y_hat, y_test, 'Logistic')

    rfc = RandomForestClassfier(n_estimators=100)
    rfc.fit(x_train, y_train)
    y_hat = rfc.predict(x_test)
    rfc_rate = show_accuracy(y_hat, y_test, 'RF')

    data_train = xgb.DMatrix(x_train, label=y_train)
    data_test = xgb.DMatrix(x_test, label=y_test)
    watch_list = [(data_test, 'evsl'), (data_train, 'train')]
    param = {'max_depth': 3, 'eta': 0.1, 'slient': 1, 'objective': 'binary:logistic'}
    bst = xgb.train(param, data_train, num_boost_round=100, evals=watch_list)
    y_hat = bst.predict(x_test)
    y_hat[y_hat > 0.5] = 1
    y_hat[~(y_hat > 0.5)] = 0
    xgb_rate = show_accuracy(y_hat, y_test, 'XGBoost')

    print 'Logistic: %.3f%%' % lr_rate
    print 'RF: %.3f%%' % rfc_rate
    print 'Logistic: %.3f%%' % xgb_rate
