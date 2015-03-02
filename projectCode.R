library(Hmisc)
library(data.table)
library(dplyr)
library(lubridate)
library(stringi)
library(stringr)
library(caret)
library(ggplot2)
library(ade4)
library(stats)
library(FactoMineR)

# Look at PCA in users dataset 

setwd('/Users/Aluminum/Documents/Machine Learning/Project')
train <- read.csv('train.csv')
users <- fread('users.csv')
words <- read.csv('words.csv')
test <- read.csv('test.csv')

# How many users are in the training/test set but not the users.csv file?
us_train <- filter(train, User %nin% users$RESPID)
us_test <- filter(test, User %nin% users$RESPID)

# Number of unique users not in train/test not in users.csv
length(unique(us_train$User))
length(unique(us_test$User))

# Percent of users in train/test not in users.csv
nrow(us_train)/nrow(train)
nrow(us_test)/nrow(test)

# Percent of unique users in train/test not in users.csv
length(unique(us_train$User))/length(unique(train$User))
length(unique(us_test$User))/length(unique(test$User))

# Frequencies of feature levels:
gender <- data.frame(table(users$GENDER))
"Female: 24503
Male: 24142"

working <- data.frame(table(users$WORKING))
"1                                                        13125
2                               Employed 30+ hours a week 13617
3                            Employed 8-29 hours per week  4086
4           Employed part-time less than 8 hours per week   385
5                      Full-time housewife / househusband  2627
6                                       Full-time student  5105
7              In unpaid employment (e.g. voluntary work)   341
8                                                   Other  1413
9                                       Part-time student   219
10                                    Prefer not to state   235
11 Retired from full-time employment (30+ hours per week)  3292
12                           Retired from self-employment   384
13                                          Self-employed  1929
14                                 Temporarily unemployed  1887"

region <- data.frame(table(users$REGION))
"              Var1  Freq
1                   1040
2           Centre  2846
3         Midlands 11844
4            North 16741
5    North Ireland   138
6 Northern Ireland   769
7            South 15267"

music <- data.frame(table(users$MUSIC))
"                                                                                         Var1  Freq
1                                     I like music but it does not feature heavily in my life 11790
2                                                     Music has no particular interest for me  1037
3                                 Music is important to me but not necessarily more important 16659
4 Music is important to me but not necessarily more important than other hobbies or interests  2473
5                                      Music is no longer as important as it used to be to me  1604
6                                            Music means a lot to me and is a passion of mine 15082"

list.own <- data.frame(table(users$LIST_OWN)) # This variable has been cleaned up
"        Var1  Freq
1             5939
2    0 hours 10946
3     1 hour 10653
4   10 hours   537
5   11 hours    57
6   12 hours   233
7   13 hours    30
8   14 hours    56
9   15 hours    63
10  16 hours    33
11 16+ hours   535
12   2 hours  9397
13   3 hours  4269
14   4 hours  2549
15   5 hours  1454
16   6 hours   846
17   7 hours   341
18   8 hours   572
19   9 hours   135"

list.back <- data.frame(table(users$LIST_BACK)) # Similarly messy and needs to be cleaned up
"        Var1 Freq
1            5825
2    0 hours 9298
3     1 hour 8392
4   10 hours  768
5   11 hours   96
6   12 hours  369
7   13 hours   50
8   14 hours   95
9   15 hours   92
10  16 hours   53
11 16+ hours  777
12   2 hours 8298
13   3 hours 4584
14   4 hours 3408
15   5 hours 2154
16   6 hours 1692
17   7 hours  833
18   8 hours 1480
19   9 hours  381"

# Cleaning up LIST_OWN and LIST_BACK
users <- data.frame(users)

no = c('')
zero = c('0', '0 Hours', 'Less than an hour')
one = c('1', '1 hour')
two = c('2', '2 hours')
three = c('3', '3 hours')
four = c('4', '4 hours')
five = c('5', '5 hours')
six = c('6', '6 hours')
seven = c('7', '7 hours')
eight = c('8', '8 hours')
nine = c('9', '9 hours')
ten = c('10', '10 hours')
eleven = c('11', '11 hours')
twelve = c('12', '12 hours')
thirteen = c('13', '13 hours')
fourteen = c('14', '14 hours')
fifteen = c('15', '15 hours')
sixteen = c('16', '16 hours')
sixteenPlus = c('16+ hours', 'More than 16 hours', '17', '18', '19', '20', '21', '22', '23', '24')

lono <- filter(users, LIST_OWN %in% no)
lo00 <- filter(users, LIST_OWN %in% zero)
lo00 <- mutate(lo00, LIST_OWN = 0)
lo01 <- filter(users, LIST_OWN %in% one)
lo01 <- mutate(lo01, LIST_OWN = 1)
lo02 <- filter(users, LIST_OWN %in% two)
lo02 <- mutate(lo02, LIST_OWN = 2)
lo03 <- filter(users, LIST_OWN %in% three)
lo03 <- mutate(lo03, LIST_OWN = 3)
lo04 <- filter(users, LIST_OWN %in% four)
lo04 <- mutate(lo04, LIST_OWN = 4)
lo05 <- filter(users, LIST_OWN %in% five)
lo05 <- mutate(lo05, LIST_OWN = 5)
lo06 <- filter(users, LIST_OWN %in% six)
lo06 <- mutate(lo06, LIST_OWN = 6)
lo07 <- filter(users, LIST_OWN %in% seven)
lo07 <- mutate(lo07, LIST_OWN = 7)
lo08 <- filter(users, LIST_OWN %in% eight)
lo08 <- mutate(lo08, LIST_OWN = 8)
lo09 <- filter(users, LIST_OWN %in% nine)
lo09 <- mutate(lo09, LIST_OWN = 9)
lo10 <- filter(users, LIST_OWN %in% ten)
lo10 <- mutate(lo10, LIST_OWN = 10)
lo11 <- filter(users, LIST_OWN %in% eleven)
lo11 <- mutate(lo11, LIST_OWN = 11)
lo12 <- filter(users, LIST_OWN %in% twelve)
lo12 <- mutate(lo12, LIST_OWN = 12)
lo13 <- filter(users, LIST_OWN %in% thirteen)
lo13 <- mutate(lo13, LIST_OWN = 13)
lo14 <- filter(users, LIST_OWN %in% fourteen)
lo14 <- mutate(lo14, LIST_OWN = 14)
lo15 <- filter(users, LIST_OWN %in% fifteen)
lo15 <- mutate(lo15, LIST_OWN = 15)
lo16 <- filter(users, LIST_OWN %in% sixteen)
lo16 <- mutate(lo16, LIST_OWN = 16)
loUp <- filter(users, LIST_OWN %in% sixteenPlus)
loUp <- mutate(loUp, LIST_OWN = 16)
users <- rbind(lono, lo00, lo01, lo02, lo03, lo04, lo05, lo06, lo07, lo08, lo09, lo10, lo11, lo12, lo13,
               lo14, lo15, lo16, loUp)

lbno <- filter(users, LIST_BACK %in% no)
lb00 <- filter(users, LIST_BACK %in% zero)
lb00 <- mutate(lb00, LIST_BACK = 0)
lb01 <- filter(users, LIST_BACK %in% one)
lb01 <- mutate(lb01, LIST_BACK = 1)
lb02 <- filter(users, LIST_BACK %in% two)
lb02 <- mutate(lb02, LIST_BACK = 2)
lb03 <- filter(users, LIST_BACK %in% three)
lb03 <- mutate(lb03, LIST_BACK = 3)
lb04 <- filter(users, LIST_BACK %in% four)
lb04 <- mutate(lb04, LIST_BACK = 4)
lb05 <- filter(users, LIST_BACK %in% five)
lb05 <- mutate(lb05, LIST_BACK = 5)
lb06 <- filter(users, LIST_BACK %in% six)
lb06 <- mutate(lb06, LIST_BACK = 6)
lb07 <- filter(users, LIST_BACK %in% seven)
lb07 <- mutate(lb07, LIST_BACK = 7)
lb08 <- filter(users, LIST_BACK %in% eight)
lb08 <- mutate(lb08, LIST_BACK = 8)
lb09 <- filter(users, LIST_BACK %in% nine)
lb09 <- mutate(lb09, LIST_BACK = 9)
lb10 <- filter(users, LIST_BACK %in% ten)
lb10 <- mutate(lb10, LIST_BACK = 10)
lb11 <- filter(users, LIST_BACK %in% eleven)
lb11 <- mutate(lb11, LIST_BACK = 11)
lb12 <- filter(users, LIST_BACK %in% twelve)
lb12 <- mutate(lb12, LIST_BACK = 12)
lb13 <- filter(users, LIST_BACK %in% thirteen)
lb13 <- mutate(lb13, LIST_BACK = 13)
lb14 <- filter(users, LIST_BACK %in% fourteen)
lb14 <- mutate(lb14, LIST_BACK = 14)
lb15 <- filter(users, LIST_BACK %in% fifteen)
lb15 <- mutate(lb15, LIST_BACK = 15)
lb16 <- filter(users, LIST_BACK %in% sixteen)
lb16 <- mutate(lb16, LIST_BACK = 16)
lbUp <- filter(users, LIST_BACK %in% sixteenPlus)
lbUp <- mutate(lbUp, LIST_BACK = 16)
users <- rbind(lbno, lb00, lb01, lb02, lb03, lb04, lb05, lb06, lb07, lb08, lb09, lb10, lb11, lb12, lb13,
               lb14, lb15, lb16, lbUp)
users$LIST_OWN <- as.integer(users$LIST_OWN)
users$LIST_BACK <- as.integer(users$LIST_BACK)

# GENDER as dummy variable
male <- filter(users, GENDER == 'Male')
female <- filter(users, GENDER == 'Female')
male$GENDER = 1
female$GENDER = 0
users <- rbind(male, female)

write.csv(users, 'users_int.csv')

# Creating some dummy variables
users <- data.frame(users)
dummy <- acm.disjonctif(users[c('GENDER', 'WORKING', 'REGION', 'MUSIC', 'LIST_OWN', 'LIST_BACK')])
nodummy <- select(users, -c(2, 4:8))
new_users <- cbind(nodummy, dummy)

write.csv(new_users, 'users_pretty_dummy.csv')

setwd('/Users/Aluminum/Documents/Machine Learning/MSAN630_music/data')
users <- fread('users_pretty_dummy.csv')
users <- data.frame(select(users, -1))

# FactoMineR
users.pca <- PCA(users[2:87])
summary(users.pca)
users.pcaQs <- PCA(users[3:21])
summary(users.pcaQs)
users.pcaLIST_BACK <- PCA(users[70:88])
summary(users.pcaLIST_BACK)
users.pcaLIST_OWN <- PCA(users[51:69])
summary(users.pcaLIST_OWN)
users.pcaREGION <- PCA(users[38:44])
summary(users.pcaREGION)
users.pcaWORKING <- PCA(users[24:37])
summary(users.pcaWORKING)
