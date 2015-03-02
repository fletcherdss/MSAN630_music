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
users = pd.read_csv('data/users_pretty.csv')


# merging data by userID, so have augmented data
newTestData = pd.merge(testData, users, left_on='User', right_on='RESPID', how='left')
newTrainData = pd.merge(trainData, users, left_on='User', right_on='RESPID', how='left')
n = range(len(newTestData))
# print len(newTestData) # 125794 rows
# print newTestData.head(), '\n'


# creating random indices
np.random.seed(0)
sampleIndex = np.random.choice(n, 1000, replace=False)
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


newTrainData = newTrainData.loc[sampleIndex]
newTrainData = newTrainData.reset_index()
print newTrainData.shape
print newTrainData, '\n'

data = pd.DataFrame({'init': [0]*len(newTrainData)})
print data

for i in newTrainData.columns:
    if newTrainData[i].dtype.name == 'object':
        if i == 'LIST_OWN':
            newData = pd.get_dummies(newTrainData[i], prefix='own')
        elif i == 'LIST_BACK':
            newData = pd.get_dummies(newTrainData[i], prefix='back')
        else: newData = pd.get_dummies(newTrainData[i])
        data = data.join(newData)
    else:
        data = data.join(newTrainData[i])

data = data.drop('init', axis=1)
print data.columns