import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, RegressorMixin



#This has not yet been fully tested for compatibility, see: 
#http://scikit-learn.org/stable/developers/index.html#rolling-your-own-estimator
#Specifically this will fail on any function which requires cloning 
#IE crossvalidation 


#A simple regression model which always
#predicts the mean of the target variable
class MeanPredictor(BaseEstimator, RegressorMixin):
    def __init__(self, mu = 0):
        self.mu = mu
        self.X = None

    def fit(self, X, y):
        self.mu = np.mean(y)
        self.X = X
        return self
        
    def predict(self, X):
        return np.full(len(X), self.mu)

    def __repr__(self):
        return "MeanPredictor with mean = {}".format(self.mu)


class ModelStump(BaseEstimator, RegressorMixin):
    '''
    Splitting Model: Like a decision stump with an additional model at the leaves
    
    A simple model framework for splitting on features and
    then regressing individually
    
    Parameters
    ----------
    model_constructor : Sklearn Regressor, default = MeanPredictor 

    splitInds : The column indicies of the categorical variables being split on.
       A split on classes C_1 ... C_n with produce |C_1 x C_2 x ... x C_n| splits

    verbose : default = False

    partial_keys : [(C_1, C_2, ..., C_n)], default = None
       If the split classes are known it is possible to give
       a partial list. For testing models without training on the full data set

    
    '''
    def __init__(self, model_constructor = MeanPredictor,
                  splitInds = None, verbose = False, partial_keys = None):
        self.predictors = {}
        self.splitInds = splitInds

        # The variables we are splitting on
        self.splitVars = None

        # The features used for prediction
        self.features = None

        self.model = model_constructor
        self.verbose = verbose

        
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
        for i, (key, subframe) in enumerate(df.groupby(splitVars)):
            m = self.model()

            X = np.asarray(subframe[self.features])
            y = np.asarray(subframe[target])
            m.fit(X, y)
            self.predictors[key] = m
            if self.verbose:
                print "model", i, "fitted"
        return self
            
    def fit(self, X, y):
        if self.splitInds is None:
            print "warning: split variables not specified"
            self.splitInds = []
        d = pd.DataFrame(X)
        d['y'] = y
        self.fit_df(d, self.splitInds, 'y')
        return self
            
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

class TargetAdjuster(BaseEstimator, RegressorMixin):
    def __init__(self, model_constructor = MeanPredictor, 
                 groupIndex = None, groupFeature = None):
        self.baseModel = model_constructor
        self.groupIndex = groupIndex
        self.groupFeature = groupFeature
        self.predictor = None
        self.means = None
        self.global_mean = None

    def fit_df(self, df, target_name):
        gr = df[[self.groupFeature, target_name]].groupby(self.groupFeature, as_index = False)
        grag = gr.aggregate(np.mean)
        data = pd.merge(df, grag, 'left', left_on = self.groupFeature,
                        right_on = self.groupFeature, suffixes = ('', '_mean'))
        data[target_name + '_relative'] = data[target_name] - data[target_name + '_mean']
        relevant_vars = lambda c: (c not in [self.groupFeature, target_name,
                                             target_name + '_mean', target_name + '_relative'])
        X = np.array(data[filter(relevant_vars, data.columns)]  )
        y = np.array(data[target_name + '_relative'])
        m = self.baseModel()
        m.fit(X, y)
        self.predictor = m
        self.means = dict((a,b) for _, a, b in grag.itertuples())
        self.global_mean = np.mean(y)
        return self

    def fit(self, X, y):
        if self.groupIndex is None:
            print "warning: groupVariable not specified, defaulting to first column"
            self.groupIndex = 0
        self.groupFeature = self.groupIndex
        d = pd.DataFrame(X)
        d['y'] = y
        self.fit_df(d, 'y')
        return self

    def predict(self, X):
        Xt = X.T
        group = Xt[self.groupIndex]
        X2 = np.delete(Xt, self.groupIndex, 0).T
        y_rel = self.predictor.predict(X2)
        y_means = np.array([self.means[u] if u in self.means else self.global_mean for u in group ])
        return y_rel + y_means
        
def test1():
    t = TargetAdjuster(groupIndex = 2)
    data = pd.read_csv("data/train.csv")
    #t.fit_df(data, 'Rating')
    X = np.array(data[['Artist', 'Track', 'User']])
    y = np.array(data['Rating'])
    t.fit(X, y)

    return t.score(X, y)

    
if __name__ == "__main__":
    data = pd.read_csv("data/train.csv")
    groups = data.groupby(["Artist", "Track"])
    
    d = pd.DataFrame()
    d["Artist"] = [1,1,1,1,2,2,2,2,2] 
    d["Track"] =  [1,2,3,4,1,1,2,2,6] 
    d["Rating"] = [100,100,50,50,40,50,60,70,80] 
    
    g = d.groupby(["Artist", "Track"])
