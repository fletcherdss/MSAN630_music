from sklearn.cross_validation import KFold
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import Imputer
from sklearn.cross_validation import cross_val_score
from sklearn.linear_model import Ridge
from sklearn.decomposition import PCA
from sklearn.preprocessing import normalize
import pandas as pd
from regress import ModelStump, MeanPredictor, TargetAdjuster
import numpy as np



def readData(comp1 = 39, comp2 = 19, normal = False, id_cols = [1, 2, 3]):
    data = pd.read_csv("data/train_words_users_PCAed.csv")
    data = data.fillna(0)
    y = np.asarray(data["Rating"])
    if not normal:
        X = np.asarray(data.icol([1, 2, 3] + range(5, 6 + comp1) + range(45, 76 + comp2)))
    else:
        X = normalize(np.asarray(data.icol(range(5, 6 + comp1) + range(45, 76 + comp2))), axis = 1)
        X = np.concatenate((np.asarray(data.icol(id_cols)), X), axis = 1)

    return X, y


def test_base(comp):
    X, y = readData(10, 5)
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
#[ 0.11494427  0.24207412  0.31433313]

def test_ridge(comp1, comp2):
    X, y = readData(comp1, comp2)
    print "data read"
    scores = np.zeros(4)
    for i, (train, test) in enumerate(KFold(len(X), 20, shuffle = True)):
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

    return scores/20

#print test_ridge(39, 19)
#[ 0.41191868  0.43856074  0.28469428 Na]
#print test_ridge(10, 5)
#[ 0.39208754  0.44186485  0.37996112  0.31037785]
#0.392063874155 0.442124577268
#print test_ridge(4, 3)
#a, b = 0, 0
#for i in range(5):
#    x, y, _, __ = test_ridge(10, 5)
#    a += x
#    b += y
#print a/5, b/5
#0.392063874155 0.442124577268


def test_Forest(comp1, comp2):
    X, y = readData(comp1, comp2)
    print "data read"
    scores = np.zeros(3)
    for i, (train, test) in enumerate(KFold(len(X), 20)):
        m1 = RandomForestRegressor(min_samples_split = 10, n_estimators = 10, n_jobs = -1) 
        m2 = ModelStump(lambda: 
                        RandomForestRegressor(min_samples_split = 20) , [0, 1])

        m3 = TargetAdjuster(lambda : 
                             RandomForestRegressor(min_samples_split = 20), groupIndex = 2)
        m4 = TargetAdjuster(lambda : 
                    ModelStump(lambda: 
                        RandomForestRegressor(min_samples_split = 20) , [0, 1]), groupIndex = 2)

        print "fold", i
        for j, m in enumerate([m2]):
            m.fit(X[train], y[train])
            s = m.score(X[test], y[test])
            scores[j] += s
            print s

    print scores/20


print test_Forest(10, 5)
#[ 0.50527151  0.43637286  0.        ]


#print test_Forest(4, 1)


def test_KNN(comp1, comp2, norm = False):
    X, y = readData(comp1, comp2)
    print "data read"
    scores = np.zeros(3)
    for i, (train, test) in enumerate(KFold(len(X), 20, shuffle = True)):
        m1 = KNeighborsRegressor(30)
        m2 = ModelStump(lambda : KNeighborsRegressor(30), [0, 1])
        m3 = TargetAdjuster(lambda : KNeighborsRegressor(30), groupIndex = 2)
        print "fold", i
        for j, m in enumerate([m1, m2, m3]):
            m.fit(X[train], y[train])
            s = m.score(X[test], y[test])
            scores[j] += s
            print s

    print scores/20

def test_KNN_base(comp1, comp2, norm = False):
    X, y = readData(comp1, comp2, norm, [])
    print "data read"
    scores = np.zeros(3)
    for i, (train, test) in enumerate(KFold(len(X), 20, shuffle = True)):
        m1 = KNeighborsRegressor(30)
        print "fold", i
        for j, m in enumerate([m1]):
            m.fit(X[train], y[train])
            s = m.score(X[test], y[test])
            scores[j] += s
            print s

    print scores/20

def test_KNN_split(comp1, comp2, norm = False):
    X, y = readData(comp1, comp2, norm, [1,2])
    print "data read"
    scores = np.zeros(3)
    for i, (train, test) in enumerate(KFold(len(X), 20, shuffle = True)):
        m2 = ModelStump(lambda : KNeighborsRegressor(30), [0, 1])
        print "fold", i
        for j, m in enumerate([m2]):
            m.fit(X[train], y[train])
            s = m.score(X[test], y[test])
            scores[j] += s
            print s

    print scores/20


def test_KNN_adj(comp1, comp2, norm = False):
    X, y = readData(comp1, comp2, norm, [1, 2, 3])
    print "data read"
    scores = np.zeros(3)
    for i, (train, test) in enumerate(KFold(len(X), 20, shuffle = True)):
        m3 = TargetAdjuster(lambda : KNeighborsRegressor(30), groupIndex = 2)
        print "fold", i
        for j, m in enumerate([m3]):
            m.fit(X[train], y[train])
            s = m.score(X[test], y[test])
            scores[j] += s
            print s

    print scores/20



#test_KNN(10, 5, False)
#[ 0.15892183  0.11194273  0.34372239]
#test_KNN_base(10, 5, True)
#[ 0.4117381  0.         0.       ]
 

#test_KNN_split(10, 5, True)
#[ 0.37540765  0.          0.        ]
#test_KNN_adj(10, 5, True)
#[ 0.36359381  0.          0.        ]
