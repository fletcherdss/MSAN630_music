__author__ = 'stevenchu'

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn import tree
from sklearn import linear_model
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import AdaBoostClassifier


# reading in data from testing as well as users csv
trainData = pd.read_csv("data/train.csv")
testData = pd.read_csv("data/test.csv")
users = pd.read_csv('data/users_pretty.csv')


# merging data by userID, so have augmented data
newTestData = pd.merge(testData, users, left_on='User', right_on='RESPID', how='left')
newTrainData = pd.merge(trainData, users, left_on='User', right_on='RESPID', how='left')
n = range(len(newTestData))
# print len(newTestData) # 125794 rows
# print newTestData.head(), '\n'


# creating random indices
np.random.seed(0)
sampleIndex = np.random.choice(n, 10000, replace=False)
# print sampleIndex, '\n'


# taking actual random sample of data
sampleData = newTestData.loc[sampleIndex]
# print len(sampleData)
# print sampleData.head(), '\n'


# iterating through new data
# let's keep track (counter) of the number of other users who've listened to that particular artist/track
'''
counter = []
for index, row in sampleData.iterrows():
    artist = row['Artist']
    track = row['Track']

    trainingData = newTrainData[(newTrainData['Artist'] == artist) & (newTrainData['Track'] == track)]
    counter.append(len(trainingData))

plt.hist(counter, bins=50)
plt.show()
'''



for index, row in sampleData.iterrows():
    artist = row['Artist']
    track = row['Track']

    trainingData = newTrainData[(newTrainData['Artist'] == artist) & (newTrainData['Track'] == track)]
    target = trainingData['Rating']

    trainingData = trainingData.drop('Rating', axis=1)

    # print trainingData.dtypes
    # print set(trainingData['Unnamed: 0'])
    # print set(trainingData['RESPID'])
    # print set(trainingData['AGE'])
    # print set(trainingData['Q1'])
    # print set(trainingData['Q2'])
    # print set(trainingData['Q3'])
    # print set(trainingData['Q4'])
    # print set(trainingData['Q5'])
    # print set(trainingData['Q6'])
    # print set(trainingData['Q7'])
    # print set(trainingData['Q8'])
    # print set(trainingData['Q9'])
    # print set(trainingData['Q10'])
    # print set(trainingData['Q11'])
    # print set(trainingData['Q12'])
    # print set(trainingData['Q13'])
    # print set(trainingData['Q14'])
    # print set(trainingData['Q15'])
    # print set(trainingData['Q16'])
    # print set(trainingData['Q17'])
    # print set(trainingData['Q18'])
    # print set(trainingData['Q19'])

    # clf = tree.DecisionTreeRegressor()
    # clf.fit(trainingData, target)
    # print clf.predict(row)

    # regr = linear_model.LinearRegression()
    # regr.fit(trainingData, target)
    # print regr.predict(row)