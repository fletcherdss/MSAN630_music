__author__ = 'stevenchu'

import numpy as np
import pandas as pd

from regress import ModelStump, MeanPredictor

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import Imputer
from sklearn.cross_validation import KFold
from sklearn.cross_validation import cross_val_score

from sklearn.svm import SVR, NuSVR
from sklearn.linear_model import Ridge
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression



# reading in data from testing as well as users csv
trainData = pd.read_csv("data/train.csv")
testData = pd.read_csv("data/test.csv")
users = pd.read_csv('data/users_pretty_dummy.csv')


# merging data to have more things together
newTestData = pd.merge(testData, users, left_on='User', right_on='RESPID', how='left')
newTrainData = pd.merge(trainData, users, left_on='User', right_on='RESPID', how='left')
newTrainData.fillna(newTrainData.mean(), inplace=True)


# this is a test of splitting, not including
# any information about the user
def test1():
    for i, (train, test) in enumerate(KFold(len(newTrainData), 5)):
        d_train = newTrainData.iloc[train]
        d_test = newTrainData.iloc[test]

        X = np.asarray(newTrainData)
        y = np.asarray(newTrainData['Rating'])

        m1 = ModelStump(MeanPredictor, [0, 1])
        m2 = ModelStump()
        m3 = ModelStump(lambda: KNeighborsRegressor(30), [0, 1])

        m1.fit(X[train], y[train])
        m2.fit_df(d_train, ["Artist"], 'Rating')
        m3.fit(X[train], y[train])

        R21 = m1.score(X[test], y[test])
        R22 = m2.score(X[test], y[test])
        R23 = m2.score(X[test], y[test])

        print "Fold", (i + 1)
        print "By Artist", R22
        print "By Song", R21
        print "By Song With KNN 30", R23, '\n'

# see http://scikit-learn.org/stable/auto_examples/imputation.html#example-imputation-py
# for dealing with missing values



'''
def test3()
    train = pd.read_csv("data/train.csv")
    users = pd.read_csv("data/users.csv")
    data = pd.merge(train, users, 'left', left_on = 'User', right_on = 'RESPID')
    X = np.asarray(data[["Artist", "Track"] + ["Q" + str(i) for i in range(1,20)]])
    y = data.Rating
'''



target = newTrainData['Rating']
newTrainData = newTrainData.drop('Rating', axis=1)

def test2():
    for i, (train, test) in enumerate(KFold(len(newTrainData), 5)):

        X = np.asarray(newTrainData)
        y = np.asarray(target)

        m1 = ModelStump(MeanPredictor, [0, 1])
        m2 = ModelStump(lambda: DecisionTreeRegressor(max_depth = 3), [0, 1])
        m3 = ModelStump(lambda: KNeighborsRegressor(30), [0, 1])
        m4 = ModelStump(lambda: Ridge(), [0, 1], verbose = False)
        m5 = Ridge()
        m6 = ModelStump(lambda: LinearRegression(), [0, 1])

        m1.fit(X[train], y[train])
        m2.fit(X[train], y[train])
        m3.fit(X[train], y[train])
        m4.fit(X[train], y[train])
        m5.fit(X[train], y[train])
        m6.fit(X[train], y[train])

        R21 = m1.score(X[test], y[test])
        R22 = m2.score(X[test], y[test])
        R23 = m3.score(X[test], y[test])
        R24 = m4.score(X[test], y[test])
        R25 = m5.score(X[test], y[test])
        R26 = m6.score(X[test], y[test])

        print "Fold:", (i + 1)
        print "By Song:", R21
        print "By Song Decision Tree:", R22
        print "By Song With KN 30:", R23
        print "By Song With Ridge:", R24
        print "Ridge:", R25
        print "Linear Regression:", R26, '\n'


if __name__ == "__main__":
    # test1()
    test2()



