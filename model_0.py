__author__ = 'stevenchu'
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn import tree
from sklearn import linear_model
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import RandomForestClassifier


# reading in data from testing as well as users csv
trainData = pd.read_csv("data/train.csv")
testData = pd.read_csv("data/test.csv")
users = pd.read_csv('data/users_pretty_dummy.csv')


newTestData = pd.merge(testData, users, left_on='User', right_on='RESPID', how='left')
newTrainData = pd.merge(trainData, users, left_on='User', right_on='RESPID', how='left')

# print len(newTestData.columns)
# print newTestData.columns, '\n'

# print len(newTrainData.columns)
# print newTrainData.columns, '\n'

n = range(len(newTestData))
np.random.seed(0)
sampleIndex = np.random.choice(n, 10000, replace=False)

sampleData = newTestData.loc[sampleIndex]
sampleData.reset_index()

# print sampleData.head()

sampleData.fillna(0, inplace=True)

# print sampleData.head()


for index, row in sampleData.iterrows():
    artist = row['Artist']
    track = row['Track']

    trainingData = newTrainData[(newTrainData['Artist'] == artist) & (newTrainData['Track'] == track)]
    trainingData.fillna(0, inplace=True)
    target = trainingData['Rating']

    trainingData = trainingData.drop('Rating', axis=1)

    clf = tree.DecisionTreeRegressor()
    clf.fit(trainingData, target)
    print 'prediction:', clf.predict(row)

    # regr = linear_model.LinearRegression()
    # regr.fit(trainingData, target)
    # print 'prediction:', regr.predict(row)

    # clf = RandomForestRegressor(n_estimators=10)
    # clf = clf.fit(trainingData, target)
    # print 'prediction:', clf.predict(row)