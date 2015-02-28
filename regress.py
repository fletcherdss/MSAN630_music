
import pandas as pd
import numpy as np


#A simple regression model which always
#predicts the mean of the target variable
class MeanPredictor(object):
    def __init__(self, mu = 0):
        self.mu = mu
        self.X = None

    def fit(self, X, y):
        self.mu = np.mean(y)
        self.X = X
        
    def predict(self, X):
        return np.full(len(X), self.mu)

    def score(self, X, y):
        return np.mean((self.predict(X) - y)**2)

    def __repr__(self):
        return "MeanPredictor with mean = {}".format(self.mu)


#A simple model framework for splitting on features and
#then classifying individually
class ModelStump(object):
    def __init__(self, model_constructor = MeanPredictor, splitInds = None):
        self.predictors = {}
        self.splitInds = splitInds

        # The variables we are splitting on
        self.splitVars = None

        # The features used for prediction
        self.features = None

        self.model = model_constructor
        
    #This is assuming the input is a pandas Data Frame
    def fit_df(self, df, splitVars, target):
        #Clear out the old predictors 
        self.predictors = {}

        self.splitVars = splitVars
        self.features = [v for v in df.columns if  v != target]
        
        #Internally we will be storing the data in a matrix
        #rather than a data frame. Thus we need to keep
        #track of the indicies of the splitting variables
        self.splitInds = [i for i, v in enumerate(self.features) if v in splitVars]             
        
        for key, subframe in df.groupby(splitVars):
            m = self.model()

            X = np.asarray(subframe[self.features])
            y = np.asarray(subframe[target])
            m.fit(X, y)
            self.predictors[key] = m

    def fit(X, y):
        if self.splitInds is None:
            print "warning: split variables not specified"
            self.splitInds = []
        d = pd.DataFrame(X)
        d['y'] = y
        self.fit_df(d, self.splitInds, 'y')
            
    def predict_df(self, df):
        X = np.asarray(df[self.features])
        return self.predict(X)
                
    def predict_row(self, x):
        key = tuple(x[i] for i in self.splitInds)
        if len(key) == 1:
            key = key[0]
        m = self.predictors[key]
        return m.predict(np.array([x]))[0]

    #This could be optimized by vectorizing
    def predict(self, X):
        yhat = np.empty(len(X))
        for i in range(len(X)):
            yhat[i] = self.predict_row(X[i])
        return yhat

    def score_df(self, df, target):
        y = df[target]
        yhat = self.predict_df(df)
        return np.mean((y - yhat)**2)
        
    def score(self, X, y):
        yhat = predict(X)
        return np.mean((y - yhat)**2)
                
#    def predict(self, X):
#        if len(X) > 0:
#            key = tuple(X[0][i] for i in self.splitInds)
#            m = self.predictors[key]
#            return m.predict(X)
#        return np.empty(0)
 
if __name__ == "__main__":
    data = pd.read_csv("data/train.csv")
    groups = data.groupby(["Artist", "Track"])
    
    d = pd.DataFrame()
    d["Artist"] = [1,1,1,1,2,2,2,2,2] 
    d["Track"] =  [1,2,3,4,1,1,2,2,6] 
    d["Rating"] = [100,100,50,50,40,50,60,70,80] 
    
    g = d.groupby(["Artist", "Track"])
