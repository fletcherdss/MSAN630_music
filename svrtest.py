from sklearn.cross_validation import KFold
from sklearn.preprocessing import Imputer
from sklearn.cross_validation import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.svm import SVR, NuSVR
from sklearn.linear_model import Ridge
from sklearn.decomposition import PCA
import pandas as pd
from regress import ModelStump, MeanPredictor
import numpy as np

def my_cross_val(X, y, models, folds):
    for i, (train, test) in enumerate(KFold(len(data), folds)):
        for m in models:
            m.fit(X[train], y[train])
            print "fold", (i + 1)
            print m.score(X[test], y[test])

train = pd.read_csv("data/train.csv")

#Artist 22 has the most listens
#so that one has the best chance for working

train = pd.read_csv("data/train.csv")
users = pd.read_csv("data/users.csv")
data = pd.merge(train, users, 'left', left_on = 'User', right_on = 'RESPID')
data2 = data[data['Artist' == 22]]

Xs = np.asarray(data2[["Artist", "Track"]])
Xr =  np.asarray(data2[["Q" + str(i) for i in range(1,20)]])
y = np.asarray(data2["Rating"])
imp = Imputer()
Xi = imp.fit_transform(Xr)
pca = PCA(n_components = comp)
Xp = pca.fit_transform(Xi)
X = np.concatenate((Xs, Xp), axis = 1)


models = [("By Song", ModelStump(MeanPredictor, [0, 1])), \
          ("By Song Decision Tree", \
            ModelStump(lambda : DecisionTreeRegressor(max_depth = 5), [0, 1])), \
          ("By Song With KN 30", ModelStump(lambda : KNeighborsRegressor(30), [0, 1])), \
          ("By Song With Ridge", ModelStump(lambda : Ridge(), [0, 1], verbose = False)), \
          ("Ridge", Ridge())]
          
my_cross_val(X, y, models, 5)
            
        
