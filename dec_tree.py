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


sampData = pd.DataFrame({'init': [0]*len(sampleData)})

for i in sampleData.columns:
    if sampleData[i].dtype.name == 'object':
        if i == 'LIST_OWN':
            newData = pd.get_dummies(sampleData[i], prefix='own')
        elif i == 'LIST_BACK':
            newData = pd.get_dummies(sampleData[i], prefix='back')
        else:
            newData = pd.get_dummies(sampleData[i])
        sampData = sampData.join(newData)
    else:
        sampData = sampData.join(sampleData[i])

sampData = sampData.drop('init', axis=1)
sampData.fillna(0, inplace=True)
# print sampData.shape
# print sampData.head()



for index, row in sampData.iterrows():
    artist = row['Artist']
    track = row['Track']

    trainingData = newTrainData[(newTrainData['Artist'] == artist) & (newTrainData['Track'] == track)]
    target = trainingData['Rating']

    trainingData = trainingData.drop('Rating', axis=1)
    trainingData = trainingData.reset_index()

    # print trainingData.dtypes, '\n'
    # print trainingData.shape

    print trainingData.shape
    print trainingData.head(), '\n'

    data_ = pd.DataFrame({'init': [0]*len(trainingData)})

    for i in trainingData.columns:
        if trainingData[i].dtype.name == 'object':
            if i == 'LIST_OWN':
                newData = pd.get_dummies(trainingData[i], prefix='own')
            elif i == 'LIST_BACK':
                newData = pd.get_dummies(trainingData[i], prefix='back')
            else:
                newData = pd.get_dummies(trainingData[i])
            data_ = data_.join(newData)
        else:
            data_ = data_.join(trainingData[i])

    data_ = data_.drop('init', axis=1)
    data_.fillna(0, inplace=True)
    print data_.shape
    print data_.head()

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

    clf = tree.DecisionTreeRegressor()
    clf.fit(data_, target)
    print clf.predict(row)

    # regr = linear_model.LinearRegression()
    # regr.fit(data_, target)
    # print regr.predict(row)

    # clf = RandomForestRegressor(n_estimators=10)
    # clf = clf.fit(trainingData, target)
    # print clf.predict(row)

    # clf = RandomForestClassifier()
    # clf = clf.fit(trainingData, target)
    # print clf.predict(row)