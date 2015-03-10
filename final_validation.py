from sklearn.cross_validation import KFold
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import Imputer
from sklearn.cross_validation import cross_val_score
from sklearn.linear_model import Ridge
from sklearn.decomposition import PCA
import pandas as pd
from regress import ModelStump, MeanPredictor, TargetAdjuster
import numpy as np



def readData(comp1 = 39, comp2 = 19):
    data = pd.read_csv("data/train_words_users_PCAed.csv")
    data = data.fillna(0)
    y = np.asarray(data["Rating"])
    X = np.asarray(data.icol([1, 2, 3] + range(5, 6 + comp1) + range(45, 76 + comp2)))
    return X, y


def test_base(comp):
    X, y = readData(None, None)
    print "data has been read"
    scores = np.zeros(3)
    for i, (train, test) in enumerate(KFold(len(X), 20)):
        m1 = ModelStump(MeanPredictor, [0, 1])
        m2 = TargetAdjuster(MeanPredictor, groupIndex = 2)
        m3 = TargetAdjuster(lambda : ModelStump(MeanPredictor, [0, 1]), groupIndex = 2)
        print "fold", i
        for j, m in enumerate([m1, m2, m3]):
            m.fit(X[train], y[train])
            s = m.score(X[test], y[test])
            scores[j] += s
            print s

    print scores/20

#print test_base(all)
#[ 0.11494427  0.15329332  0.22576763]


def test_ridge(comp1, comp2):
    X, y = readData(comp1, comp2)
    print "data read"
    scores = np.zeros(4)
    for i, (train, test) in enumerate(KFold(len(X), 20)):
        m0 = Ridge()
        m1 = ModelStump(lambda : Ridge(), [0, 1], verbose = False)
        m3 = TargetAdjuster(lambda : ModelStump(lambda: Ridge(), [0, 1]), groupIndex = 2)
        m4 = TargetAdjuster(Ridge, groupIndex = 2)
        print "fold", i
        for j, m in enumerate([m0, m1, m3, m4]):
            m.fit(X[train], y[train])
            s = m.score(X[test], y[test])
            scores[j] += s
            print s

    print scores/20

#print test_ridge(39, 19)
#[ 0.41191868  0.43856074  0.28469428 Na]
#print test_ridge(10, 5)
#[ 0.39207233  0.44164733  0.29070802  Na]
print test_ridge(10, 5)
#print test_ridge(4, 3)




def test_Forest(comp1, comp2):
    X, y = readData(comp1, comp2)
    print "data read"
    scores = np.zeros(3)
    for i, (train, test) in enumerate(KFold(len(X), 20)):
        m1 = RandomForestRegressor(min_samples_split = 200, n_estimators = 10, n_jobs = -1) 
        m2 = ModelStump(lambda: 
                        RandomForestRegressor(min_samples_split = 200) , [0, 1])

        m3 = TargetAdjuster(lambda : 
                             RandomForestRegressor(min_samples_split = 200), groupIndex = 2)
        m4 = TargetAdjuster(lambda : 
                    ModelStump(lambda: 
                        RandomForestRegressor(min_samples_split = 200) , [0, 1]), groupIndex = 2)

        print "fold", i
        for j, m in enumerate([m1, m2, m3]):
            m.fit(X[train], y[train])
            s = m.score(X[test], y[test])
            scores[j] += s
            print s

    print scores/20


#print test_Forest(10, 5)
#[ 0.50527151  0.43637286  0.        ]


#print test_Forest(4, 1)
