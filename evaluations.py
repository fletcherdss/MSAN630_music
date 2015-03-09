from sklearn.cross_validation import KFold
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import Imputer
from sklearn.cross_validation import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.svm import SVR, NuSVR
from sklearn.linear_model import Ridge
from sklearn.decomposition import PCA
import pandas as pd
from regress import ModelStump, MeanPredictor, TargetAdjuster
import numpy as np


 
#This is a test of splitting, not including
#Any information about the user 
def test1():
    data = pd.read_csv("data/train.csv")
    for i, (train, test) in enumerate(KFold(len(data), 10)):
        d_train = data.iloc[train]
        d_test = data.iloc[test]

        X = np.asarray(data[['Artist', 'Track', 'User']])
        y = np.asarray(data['Rating'])

        m1, m2 = ModelStump(MeanPredictor, [0, 1]),  ModelStump()
        m3 = ModelStump(lambda : KNeighborsRegressor(30), [0, 1])
        m4 = TargetAdjuster(groupIndex = 2)
        m5 = TargetAdjuster(lambda : ModelStump(MeanPredictor, [0, 1]), groupIndex = 2)


        m1.fit(X[train], y[train])
        m2.fit_df(d_train, ["Artist"], 'Rating')
        m3.fit(X[train], y[train])
        m4.fit(X[train], y[train])
        m5.fit(X[train], y[train])


        print "fold", (i + 1)
        R21 = m1.score(X[test], y[test])
        R22 = m2.score(X[test], y[test])
        R24 = m4.score(X[test], y[test])
        R25 = m5.score(X[test], y[test])
        print "By Artist", R22
        print "By Song", R21
        print "By user", R24
        print "By user and Song", R25
                
#see http://scikit-learn.org/stable/auto_examples/imputation.html#example-imputation-py
#for dealing with missing values
'''        
def test3()
    train = pd.read_csv("data/train.csv")
    users = pd.read_csv("data/users.csv")
    data = pd.merge(train, users, 'left', left_on = 'User', right_on = 'RESPID')
    X = np.asarray(data[["Artist", "Track"] + ["Q" + str(i) for i in range(1,20)]])
    y = data.Rating
'''


def test2():
    train = pd.read_csv("data/train.csv")
    users = pd.read_csv("data/users.csv")
    data = pd.merge(train, users, 'left', left_on = 'User', right_on = 'RESPID')
    X = np.asarray(data[["Artist", "Track"] + ["Q" + str(i) for i in range(1,20)]])
    y = np.asarray(data["Rating"])
    imp = Imputer()
    X2 = imp.fit_transform(X)

    for i, (train, test) in enumerate(KFold(len(data), 5)):
        m1 = ModelStump(MeanPredictor, [0, 1])
        m2 = ModelStump(lambda : DecisionTreeRegressor(max_depth = 3), [0, 1])
        m3 = ModelStump(lambda : KNeighborsRegressor(30), [0, 1])
        m4 = ModelStump(lambda : Ridge(), [0, 1], verbose = False)
        m5 = Ridge()

        m1.fit(X2[train], y[train])
        m2.fit(X2[train], y[train])
        m3.fit(X2[train], y[train])
        m4.fit(X2[train], y[train])
        m5.fit(X2[train], y[train])
        print "fold", (i + 1)
        R21 = m1.score(X2[test], y[test])
        R22 = m2.score(X2[test], y[test])
        R23 = m3.score(X2[test], y[test])
        R24 = m4.score(X2[test], y[test])
        R25 = m5.score(X2[test], y[test])
        print "By Song", R21
        print "By Song Decision Tree", R22
        print "By Song With KN 30", R23
        print "By Song With Ridge", R24
        print "Ridge", R25
        
    #est = Pipeline([("imputer", Imputer()),
    #                ("tree", DecisionTreeRegressor())])
    #est = ModelStump(DecisionTreeRegressor, [0, 1])
    #m3 = ModelStump(lambda : KNeighborsRegressor(30), [0, 1])

#    est.fit(X2,y)
    #score = cross_val_score(est, X2, y)
#    print est.score(X2,y)


'''
fold 1
By Song 0.111730359127
KN 30 0.101317365993
By Song With KN 30 0.169659520821
fold 2
By Song 0.112438671933
KN 30 0.104437907591
By Song With KN 30 0.168853491498
fold 3

'''

def test3(comp):
    train = pd.read_csv("data/train.csv")
    users = pd.read_csv("data/users.csv")
    data = pd.merge(train, users, 'left', left_on = 'User', right_on = 'RESPID')
    Xs = np.asarray(data[["Artist", "Track"]])
    Xr =  np.asarray(data[["Q" + str(i) for i in range(1,20)]])
    y = np.asarray(data["Rating"])
    imp = Imputer()
    Xi = imp.fit_transform(Xr)
    pca = PCA(n_components = comp)
    Xp = pca.fit_transform(Xi)
    X = np.concatenate((Xs, Xp), axis = 1)
    print "data transformed"
    for i, (train, test) in enumerate(KFold(len(data), 5)):
        m1 = ModelStump(MeanPredictor, [0, 1])
        m2 = ModelStump(lambda : DecisionTreeRegressor(max_depth = 5), [0, 1])
        m3 = ModelStump(lambda : KNeighborsRegressor(30), [0, 1])
        m4 = ModelStump(lambda : Ridge(), [0, 1], verbose = False)
        m5 = Ridge()

        m1.fit(X[train], y[train])
        m2.fit(X[train], y[train])
        m3.fit(X[train], y[train])
        m4.fit(X[train], y[train])
        m5.fit(X[train], y[train])

        print "fold", (i + 1)
        R21 = m1.score(X[test], y[test])
        R22 = m2.score(X[test], y[test])
        R23 = m3.score(X[test], y[test])
        R24 = m4.score(X[test], y[test])
        R25 = m5.score(X[test], y[test])

        print "By Song", R21
        print "By Song Decision Tree", R22
        print "By Song With KN 30", R23
        print "By Song With Ridge", R24
        print "Ridge", R25


#realized there is some subtle cheating going on here
#
def test4(comp):
    train = pd.read_csv("data/train.csv")
    users = pd.read_csv("data/users.csv")
    gr = train .groupby('User', as_index = False)
    data = pd.merge(train, (gr.aggregate(np.mean)), 'left', left_on = 'User', right_on = 'User')
    data = data[['Artist_x', 'Track_x', 'User', 'Rating_x', "Time_x", 'Rating_y']]
    data.columns = ['Artist', 'Track', 'User', 'Rating', 'Time', 'User_Average']
    data['Relative_Rating'] = data['Rating'] - data['User_Average']
    data2 = pd.merge(data, users, 'left', left_on = 'User', right_on = 'RESPID')
    print data2
    Xs = np.asarray(data2[["Artist", "Track"]])
    Xr =  np.asarray(data2[["Q" + str(i) for i in range(1,20)]])
    y = np.asarray(data2["Relative_Rating"])
    y2 = np.asarray(data2["Rating"])
    ya = np.asarray(data2["User_Average"])
    imp = Imputer()
    Xi = imp.fit_transform(Xr)
    pca = PCA(n_components = comp)
    Xp = pca.fit_transform(Xi)
    X = np.concatenate((Xs, Xp), axis = 1)
    print "data transformed"

    print "data transformed"
    for i, (train, test) in enumerate(KFold(len(X), 5)):
        m1 = ModelStump(MeanPredictor, [0, 1])
        m2 = ModelStump(lambda : DecisionTreeRegressor(max_depth = 5), [0, 1])
        m3 = ModelStump(lambda : KNeighborsRegressor(30), [0, 1])
        m4 = ModelStump(lambda : Ridge(), [0, 1], verbose = False)
        m5 = Ridge()


        m1.fit(X[train], y[train])
        m2.fit(X[train], y[train])
        m3.fit(X[train], y[train])
        m4.fit(X[train], y[train])
        m5.fit(X[train], y[train])
        print "fold", (i + 1)
        R21 = m1.score(X[test], y[test])
        R22 = m2.score(X[test], y[test])
        R23 = m3.score(X[test], y[test])
        R24 = m4.score(X[test], y[test])
        R25 = m5.score(X[test], y[test])

        yhat = m4.predict(X[test]) + ya[test]
        print len(yhat), len(y2), len(ya)
        print (np.mean((yhat - y2[test])**2))**0.5
        print 1 - (np.mean((yhat - y2[test])**2))/np.mean((y2[test] - np.mean(y2[test]))**2)



        print "By Song", R21
        print "By Song Decision Tree", R22
        print "By Song With KN 30", R23
        print "By Song With Ridge", R24
        print "Ridge", R25
    

def test5(comp):
    train = pd.read_csv("data/train.csv")
    users = pd.read_csv("data/users.csv")
    data = pd.merge(train, users, 'left', left_on = 'User', right_on = 'RESPID')
    Xs = np.asarray(data[["Artist", "Track", "User"]])
    Xr =  np.asarray(data[["Q" + str(i) for i in range(1,20)]])
    y = np.asarray(data["Rating"])
    imp = Imputer()
    Xi = imp.fit_transform(Xr)
    pca = PCA(n_components = comp)
    Xp = pca.fit_transform(Xi)
    X = np.concatenate((Xs, Xp), axis = 1)
    print "data transformed"
    for i, (train, test) in enumerate(KFold(len(data), 20)):
        m1 = ModelStump(MeanPredictor, [0, 1])
        m2 = ModelStump(lambda : DecisionTreeRegressor(max_depth = 5), [0, 1])
        m3 = ModelStump(lambda : KNeighborsRegressor(30), [0, 1])
        m4 = ModelStump(lambda : Ridge(), [0, 1], verbose = False)
        m5 = TargetAdjuster(lambda : KNeighborsRegressor(25), groupIndex = 2)
        m6 = TargetAdjuster(lambda : ModelStump(lambda: KNeighborsRegressor(15), [0, 1]), groupIndex = 2)
        m7 = TargetAdjuster(lambda : ModelStump(MeanPredictor, [0, 1]), groupIndex = 2)
        m8 = TargetAdjuster(MeanPredictor, groupIndex = 2)
        #m9 = TargetAdjuster(lambda : ModelStump(lambda: Ridge(), [0, 1]), groupIndex = 2)
        m9 = TargetAdjuster(lambda : 
                 ModelStump(lambda: RandomForestRegressor(min_samples_split = 200) , [0, 1]), groupIndex = 2)
        m10 = TargetAdjuster(lambda : RandomForestRegressor(min_samples_split = 200), groupIndex = 2)
        m11 = RandomForestRegressor(min_samples_split = 200) 
        #m9 = ModelStump(lambda: TargetAdjuster(Ridge, groupIndex = 2), [0, 1])

#TargetAdjuster(Ridge, groupIndex =  2)

        m1.fit(X[train], y[train])
        m2.fit(X[train], y[train])
        m3.fit(X[train], y[train])
        m4.fit(X[train], y[train])
        m5.fit(X[train], y[train])
        m6.fit(X[train], y[train])
        m7.fit(X[train], y[train])
        m8.fit(X[train], y[train])
        m9.fit(X[train], y[train])
        m10.fit(X[train], y[train])
        m11.fit(X[train], y[train])


        print "fold", (i + 1)
        R21 = m1.score(X[test], y[test])
        R22 = m2.score(X[test], y[test])
        R23 = m3.score(X[test], y[test])
        R24 = m4.score(X[test], y[test])
        R25 = m5.score(X[test], y[test])
        R26 = m6.score(X[test], y[test])
        R27 = m7.score(X[test], y[test])
        R28 = m8.score(X[test], y[test])
        R29 = m9.score(X[test], y[test])
        R30 = m10.score(X[test], y[test])
        R31 = m11.score(X[test], y[test])


        print "By Song", R21
        print "By Song Decision Tree", R22
        print "By Song With KN 30", R23
        print "By Song With Ridge", R24
        print "Adjusted KNN", R25
        print "by song KNN adj", R26
        print "by song Adj", R27
        print "Adj ", R28
        print "by song Adj Random Forest ", R29
        print "Adj Random Forest ", R30
        print "Random Forest ", R31


    
if __name__ == "__main__":
    train = pd.read_csv("data/train.csv")
    songs = list(set(map(tuple, list(np.asarray(train[['Artist', 'Track']])))))
    artists, tracks = zip(*songs)

    test5(5)
