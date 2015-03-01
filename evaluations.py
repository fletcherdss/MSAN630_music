from sklearn.cross_validation import KFold
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import Imputer
from sklearn.cross_validation import cross_val_score
from sklearn.pipeline import Pipeline 
import pandas as pd
from regress import ModelStump, MeanPredictor
import numpy as np

 
#This is a test of splitting, not including
#Any information about the user 
def test1():
    data = pd.read_csv("data/train.csv")
    for i, (train, test) in enumerate(KFold(len(data), 5)):
        d_train = data.iloc[train]
        d_test = data.iloc[test]

        X = np.asarray(data)
        y = data['Rating']

        m1, m2, m3 = MeanPredictor(),  ModelStump(),  ModelStump()

        m1.fit(X[train], y[train])
        m2.fit_df(d_train, ["Artist"], 'Rating')
        m3.fit_df(d_train, ["Artist", "Track"], 'Rating')

        print "fold", (i + 1)
        R21 = m1.score(X[test], y[test])
        R22 = m2.score(X[test], y[test])
        R23 = m3.score(X[test], y[test])
        print "By Artist", R22
        print "By Song", R23
        
#see http://scikit-learn.org/stable/auto_examples/imputation.html#example-imputation-py
#for dealing with missing values
        
def test3()
    train = pd.read_csv("data/train.csv")
    users = pd.read_csv("data/users.csv")
    data = pd.merge(train, users, 'left', left_on = 'User', right_on = 'RESPID')
    X = np.asarray(data[["Artist", "Track"] + ["Q" + str(i) for i in range(1,20)]])
    y = data.Rating



def test2():
    train = pd.read_csv("data/train.csv")
    users = pd.read_csv("data/users.csv")
    data = pd.merge(train, users, 'left', left_on = 'User', right_on = 'RESPID')
    data2 = data[["Artist", "Track"] + ["Q" + str(i) for i in range(1,20)] + ["Rating"]]
    for i, (train, test) in enumerate(KFold(len(data), 5)):
        d_train = data2.iloc[train]
        d_test = data2.iloc[test]
        def knn():
            return KNeighborsRegressor(10)
        m = ModelStump(DecisionTreeRegressor)
        m.fit_df(d_train, ['Artist', 'Track'], 'Rating')
        ss_res = m.score_df(d_test, 'Rating')
        print ss_res

if __name__ == "__main__":
    test1()

