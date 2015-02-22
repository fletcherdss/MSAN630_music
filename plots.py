
import pandas as pd
from collections import Counter
from ggplot import *



groups = trainData.groupby("User")
sizes = [len(g) for g in groups.groups.values()]
c = Counter(sizes)
d = pd.DataFrame()
d['size'] = sizes

#This seems to only work when it is pasted into a terminal
'''
ggplot(d, aes(x = 'size')) + geom_histogram(aes(x = 'size'), binwidth = 1) +\
    xlab('tracks heard') + ylab('number of users') +\
    ggtitle("Distribution of Number of Tracks Listened to Per User in Training Data")
ggsave("plots/user_tracks_listend.pdf")
'''
