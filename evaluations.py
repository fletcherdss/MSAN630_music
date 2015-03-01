from sklearn.cross_validation import KFold
import pandas as pd
from regress import ModelStump, MeanPredictor
import numpy as np

 
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
        print "by mean", m1.score(X[test], y[test])
        print "by artist:", m2.score_df(d_test, 'Rating')
        print "by song:", m3.score_df(d_test, 'Rating')

if __name__ == "__main__":
    test1()