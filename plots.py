
import pandas as pd
from collections import Counter
from ggplot import *


#This is really structured more like an R notebook
#Don't expect to be able to run this as a script

trainData = pd.read_csv('data/train.csv')

groups1 = trainData.groupby("User")
groups2 = trainData.groupby("Artist")
groups3 = trainData.groupby(["Artist", "Track"])

def group_keys(groups):
    sizes = [len(g) for g in groups.groups.values()]
    l = len(sizes)
    c = Counter(sizes)
    d = pd.DataFrame()
    d['size'] = sizes
    return (d,l)
    
d1, l1 = group_keys(groups1)
d2, l2 = group_keys(groups2)
d3, l3 = group_keys(groups3)

#This seems to only work when it is pasted into a terminal
'''
ggplot(d1, aes(x = 'size')) + geom_histogram(aes(x = 'size'), binwidth = 1) +\
    xlab('tracks heard') + ylab('number of users') +\
    ggtitle("Distribution of Number of Tracks Listened to Per User in Training Data")
ggsave("plots/user_tracks_listend.pdf")
'''

'''
ggplot(d2, aes(x = 'size')) + geom_histogram(aes(x = 'size'), binwidth = 500) +\
    xlab('total listens') + ylab('number of artists') +\
    ggtitle("Distribution of Artists Listend to\nTotal Artists: {}".format(l2))
ggsave("plots/artist_tracks_listend.pdf")
'''


'''
ggplot(d3, aes(x = 'size')) + geom_histogram(aes(x = 'size'), binwidth = 50) +\
    xlab('total listens') + ylab('number of songs') +\
    ggtitle("Distribution of Songs Listend to\nTotal Songs: {}".format(l3))
ggsave("plots/song_tracks_listend.pdf")
'''
