

train = pd.read_csv("data/train.csv")



#Artist 22 has the most listens
#so that one has the best chance for working

train = pd.read_csv("data/train.csv")
users = pd.read_csv("data/users.csv")
data = pd.merge(train, users, 'left', left_on = 'User', right_on = 'RESPID')
data2 = data[data['Artist' == 22]]

Xs = np.asarray(data[["Artist", "Track"]])
Xr =  np.asarray(data[["Q" + str(i) for i in range(1,20)]])
y = np.asarray(data["Rating"])
imp = Imputer()
Xi = imp.fit_transform(Xr)
pca = PCA(n_components = comp)
Xp = pca.fit_transform(Xi)
X = np.concatenate((Xs, Xp), axis = 1)
