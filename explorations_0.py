__author__ = 'stevenchu'

import pandas as pd
from collections import Counter


# userKeys is something to be looked at separately probably
# testData is what we will do our predictions on
# current thought process runs as follows: SQL queries probably necessary?
# either than or a lot of merges, which can figure out how to do in pandas

# testData = pd.read_csv('test.csv')
# print len(testData)

# userKeys = pd.read_csv('UserKey.csv')
# print userKeys.head()



# investigating size and structure of the following datasets
# intuitively how should these sizes relate to each other?
trainData = pd.read_csv('data/train.csv')
print trainData.head()
print len(trainData)

words = pd.read_csv('data/words.csv')
print words.head()
print len(words)

users = pd.read_csv('data/users.csv')
print users.head()
print len(users)



# each row in the test data will have the following information: artist, track, user, time
# we want to predict: for a given user, a given artist, and a given track, (given time?), how much user enjoys track? (scale of 0-100)

# artist: we will want a user's opinions about an artist (found by merging to words.csv file)
# track: how will we grab any information about individual tracks? not sure...
# user: we will also want demographic information about individual users
# user: furthermore, will want to know their responses to each of the questions about music
# time: how does this variable figure into things?
