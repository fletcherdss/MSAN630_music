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

setwd('/Users/Aluminum/Documents/Machine Learning/MSAN630_music')
train <- read.csv('data/train.csv')
users <- fread('data/users.csv')
words <- read.csv('data/words.csv')
test <- read.csv('data/test.csv')

# How many users are in the training/test set but not the users.csv file?
us_train <- filter(train, User %nin% users$RESPID)
us_test <- filter(test, User %nin% users$RESPID)

# Number of unique users not in train/test not in users.csv
length(unique(us_train$User)) "2278"
length(unique(us_test$User)) "2227"

# Percent of users in train/test not in users.csv
nrow(us_train)/nrow(train) "0.06283952"
nrow(us_test)/nrow(test) "0.06253875"

# Percent of unique users in train/test not in users.csv
length(unique(us_train$User))/length(unique(train$User)) "0.04603973"
length(unique(us_test$User))/length(unique(test$User)) "0.04831641"

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

dum <- acm.disjonctif(users[c('WORKING', 'REGION', 'MUSIC')])
nodum <- select(users, -c(4:6))
users <- cbind(nodum, dum)
write.csv(users, 'users_int.csv')

users <- fread('users_int.csv')
users <- data.frame(users)

pca <- PCA(users[2:51])
summary(pca)
"Eigenvalues
                       Dim.1   Dim.2   Dim.3   Dim.4   Dim.5   Dim.6   Dim.7   Dim.8   Dim.9  Dim.10  Dim.11
Variance               8.254   2.338   1.972   1.730   1.602   1.490   1.451   1.347   1.306   1.187   1.149
% of var.             16.507   4.676   3.945   3.460   3.204   2.979   2.903   2.694   2.613   2.375   2.298
Cumulative % of var.  16.507  21.183  25.128  28.587  31.791  34.770  37.673  40.367  42.980  45.355  47.652
Dim.12  Dim.13  Dim.14  Dim.15  Dim.16  Dim.17  Dim.18  Dim.19  Dim.20  Dim.21  Dim.22
Variance               1.138   1.082   1.076   1.051   1.044   1.039   1.030   1.026   1.020   1.013   1.008
% of var.              2.275   2.163   2.153   2.102   2.087   2.078   2.061   2.051   2.040   2.026   2.016
Cumulative % of var.  49.928  52.091  54.243  56.345  58.433  60.511  62.572  64.623  66.663  68.689  70.705
Dim.23  Dim.24  Dim.25  Dim.26  Dim.27  Dim.28  Dim.29  Dim.30  Dim.31  Dim.32  Dim.33
Variance               1.005   1.004   1.000   0.985   0.960   0.858   0.824   0.773   0.706   0.662   0.656
% of var.              2.011   2.008   2.000   1.970   1.921   1.716   1.647   1.546   1.412   1.323   1.313
Cumulative % of var.  72.715  74.723  76.724  78.694  80.614  82.331  83.978  85.523  86.935  88.258  89.571
Dim.34  Dim.35  Dim.36  Dim.37  Dim.38  Dim.39  Dim.40  Dim.41  Dim.42  Dim.43  Dim.44
Variance               0.614   0.567   0.531   0.501   0.477   0.393   0.369   0.333   0.322   0.269   0.248
% of var.              1.227   1.135   1.062   1.002   0.953   0.786   0.738   0.665   0.644   0.537   0.496
Cumulative % of var.  90.798  91.933  92.995  93.997  94.950  95.736  96.474  97.139  97.783  98.320  98.817
Dim.45  Dim.46  Dim.47  Dim.48  Dim.49  Dim.50
Variance               0.212   0.206   0.174   0.000   0.000   0.000
% of var.              0.423   0.413   0.347   0.000   0.000   0.000
Cumulative % of var.  99.240  99.653 100.000 100.000 100.000 100.000"

pcaWORKING <- PCA(users[25:38])
summary(pcaWORKING)
"Eigenvalues
                       Dim.1   Dim.2   Dim.3   Dim.4   Dim.5   Dim.6   Dim.7   Dim.8   Dim.9  Dim.10  Dim.11
Variance               1.379   1.214   1.106   1.081   1.063   1.048   1.041   1.032   1.011   1.008   1.007
% of var.              9.851   8.675   7.898   7.724   7.594   7.485   7.434   7.370   7.218   7.200   7.195
Cumulative % of var.   9.851  18.526  26.424  34.148  41.742  49.227  56.661  64.031  71.249  78.449  85.644
                      Dim.12  Dim.13  Dim.14
Variance               1.005   1.005   0.000
% of var.              7.180   7.176   0.000
Cumulative % of var.  92.824 100.000 100.000"

pcaREGION <- PCA(users[39:45])
summary(pcaREGION)
"Eigenvalues
                       Dim.1   Dim.2   Dim.3   Dim.4   Dim.5   Dim.6   Dim.7
Variance               1.492   1.367   1.090   1.030   1.018   1.003   0.000
% of var.             21.319  19.532  15.566  14.708  14.541  14.334   0.000
Cumulative % of var.  21.319  40.852  56.417  71.125  85.666 100.000 100.000"

pcaMUSIC <- PCA(users[46:51])
summary(pcaMUSIC)
"Eigenvalues
                       Dim.1   Dim.2   Dim.3   Dim.4   Dim.5   Dim.6
Variance               1.487   1.364   1.084   1.041   1.025   0.000
% of var.             24.777  22.734  18.069  17.342  17.077   0.000
Cumulative % of var.  24.777  47.511  65.580  82.923 100.000 100.000"

pcaOther1 <- PCA(users[2:24])
summary(pcaOther1)
"Eigenvalues
                       Dim.1   Dim.2   Dim.3   Dim.4   Dim.5   Dim.6   Dim.7   Dim.8   Dim.9  Dim.10  Dim.11
Variance               7.582   2.177   1.572   1.244   1.156   1.001   0.902   0.849   0.762   0.701   0.662
% of var.             32.965   9.467   6.836   5.411   5.028   4.352   3.924   3.690   3.312   3.049   2.879
Cumulative % of var.  32.965  42.432  49.268  54.679  59.706  64.058  67.982  71.672  74.984  78.033  80.912
                      Dim.12  Dim.13  Dim.14  Dim.15  Dim.16  Dim.17  Dim.18  Dim.19  Dim.20  Dim.21  Dim.22
Variance               0.613   0.570   0.532   0.484   0.393   0.356   0.326   0.270   0.250   0.213   0.209
% of var.              2.665   2.478   2.312   2.106   1.711   1.550   1.415   1.174   1.085   0.927   0.908
Cumulative % of var.  83.578  86.056  88.368  90.474  92.185  93.735  95.150  96.325  97.410  98.336  99.244
                      Dim.23
Variance               0.174
% of var.              0.756
Cumulative % of var. 100.000"

pcaQs <- PCA(users[6:24])
summary(pcaQs)
"Eigenvalues
                       Dim.1   Dim.2   Dim.3   Dim.4   Dim.5   Dim.6   Dim.7   Dim.8   Dim.9  Dim.10  Dim.11
Variance               7.234   2.144   1.456   1.177   0.884   0.807   0.745   0.689   0.600   0.564   0.492
% of var.             38.075  11.284   7.662   6.197   4.653   4.247   3.922   3.624   3.156   2.966   2.589
Cumulative % of var.  38.075  49.359  57.022  63.218  67.872  72.119  76.041  79.666  82.821  85.788  88.377
                      Dim.12  Dim.13  Dim.14  Dim.15  Dim.16  Dim.17  Dim.18  Dim.19
Variance               0.397   0.361   0.326   0.274   0.252   0.216   0.210   0.174
% of var.              2.089   1.898   1.718   1.440   1.325   1.136   1.103   0.915
Cumulative % of var.  90.466  92.363  94.081  95.521  96.846  97.982  99.085 100.000"

pcaOther2 <- PCA(users[2:5])
summary(pcaOther2)
"Eigenvalues
                       Dim.1   Dim.2   Dim.3   Dim.4
Variance               1.319   1.018   0.996   0.668
% of var.             32.964  25.439  24.895  16.702
Cumulative % of var.  32.964  58.403  83.298 100.000"


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


# Using full joined data, getting rid of NAs
users <- data.frame(select(fread('data/joined_train.csv'), -1))
# Getting rid of AGE NA's
age <- data.frame(table(users$AGE))
ageNA <- filter(users, AGE %nin% age$Var1)
ageNoNA <- filter(users, AGE %in% age$Var1)
meanAge <- mean(ageNoNA$AGE)
ageNA <- mutate(ageNA, AGE = meanAge)
users <- rbind(ageNA, ageNoNA)
# Getting rid of LIST_OWN NA's
listown <- data.frame(table(users$LIST_OWN))
ownNA <- filter(users, LIST_OWN %nin% listown$Var1)
ownNoNA <- filter(users, LIST_OWN %in% listown$Var1)
meanOwn <- mean(ownNoNA$LIST_OWN)
ownNA <- mutate(ownNA, LIST_OWN = meanOwn)
users <- rbind(ownNA, ownNoNA)
# Getting rid of LIST_BACK NA's
back <- data.frame(table(users$LIST_BACK))
backNA <- filter(users, LIST_BACK %nin% back$Var1)
backNoNA <- filter(users, LIST_BACK %in% back$Var1)
meanBack <- mean(backNoNA$LIST_BACK)
backNA <- mutate(backNA, LIST_BACK = meanBack)
users <- rbind(backNA, backNoNA)
# Getting rid of Q16 NA'a
q16 <- data.frame(table(users$Q16))
q16NA <- filter(users, Q16 %nin% q16$Var1)
q16NoNA <- filter(users, Q16 %in% q16$Var1)
meanQ16 <- mean(q16NoNA$Q16)
q16NA <- mutate(q16NA, Q16 = meanQ16)
users <- rbind(q16NA, q16NoNA)
# Getting rid of Q18 NA'a
q18 <- data.frame(table(users$Q18))
q18NA <- filter(users, Q18 %nin% q18$Var1)
q18NoNA <- filter(users, Q18 %in% q18$Var1)
meanQ18 <- mean(q18NoNA$Q18)
q18NA <- mutate(q18NA, Q18 = meanQ18)
users <- rbind(q18NA, q18NoNA)
# Getting rid of Q19 NA'a
q19 <- data.frame(table(users$Q19))
q19NA <- filter(users, Q19 %nin% q19$Var1)
q19NoNA <- filter(users, Q19 %in% q19$Var1)
meanQ19 <- mean(q19NoNA$Q19)
q19NA <- mutate(q19NA, Q19 = meanQ19)
users <- rbind(q19NA, q19NoNA)

write.csv(users, 'joined_train_noNA.csv')


# stats package PCA stuff
users_all <- data.frame(select(users, c(5:55)))
users.pca <- prcomp(users_all, center = TRUE, scale. = TRUE)
plot(users.pca, type = 'lines')
pca.df <- data.frame(users.pca[2])
write.csv(pca.df, 'data/all_variables_pca.csv')

users_misc <- data.frame(select(users, c(5:9)))
misc.pca <- prcomp(users_misc, center = TRUE, scale. = TRUE)
plot(misc.pca, type = 'lines')
misc.df <- data.frame(misc.pca[2])
write.csv(misc.df, 'data/misc_pca.csv')

qs <- data.frame(select(users, c(10:28)))
qs.pca <- prcomp(qs, center = TRUE, scale. = TRUE)
plot(qs.pca, type = 'lines')
qs.df <- data.frame(qs.pca[2])
write.csv(qs.df, 'data/questions_pca.csv')

work <- data.frame(select(users, c(29:42)))
work.pca <- prcomp(work, center = TRUE, scale. = TRUE)
plot(work.pca, type = 'lines')
work.df <- data.frame(work.pca[2])
write.csv(work.df, 'data/working_pca.csv')

region <- data.frame(select(users, c(43:49)))
reg.pca <- prcomp(region, center = TRUE, scale. = TRUE)
plot(reg.pca, type = 'lines')
reg.df <- data.frame(reg.pca[2])
write.csv(reg.df, 'data/region_pca.csv')

music <- data.frame(select(users, c(50:55)))
music.pca <- prcomp(music, center = TRUE, scale. = TRUE)
plot(music.pca, type = 'lines')
music.df <- data.frame(music.pca[2])
write.csv(music.df, 'data/music_pca.csv')


# Histograms
ggplot() + geom_histogram(data = users, aes(x = AGE))
ggplot() + geom_histogram(data = users, aes(x = LIST_OWN))
ggplot() + geom_histogram(data = users, aes(x = LIST_BACK))
ggplot() + geom_histogram(data = users, aes(x = Q1))
ggplot() + geom_histogram(data = users, aes(x = Q2))
ggplot() + geom_histogram(data = users, aes(x = Q3))
ggplot() + geom_histogram(data = users, aes(x = Q4))
ggplot() + geom_histogram(data = users, aes(x = Q5))
ggplot() + geom_histogram(data = users, aes(x = Q6))
ggplot() + geom_histogram(data = users, aes(x = Q7))
ggplot() + geom_histogram(data = users, aes(x = Q8))
ggplot() + geom_histogram(data = users, aes(x = Q9))
ggplot() + geom_histogram(data = users, aes(x = Q10))
ggplot() + geom_histogram(data = users, aes(x = Q11))
ggplot() + geom_histogram(data = users, aes(x = Q12))
ggplot() + geom_histogram(data = users, aes(x = Q13))
ggplot() + geom_histogram(data = users, aes(x = Q14))
ggplot() + geom_histogram(data = users, aes(x = Q15))
ggplot() + geom_histogram(data = users, aes(x = Q16))
ggplot() + geom_histogram(data = users, aes(x = Q17))
ggplot() + geom_histogram(data = users, aes(x = Q18))
ggplot() + geom_histogram(data = users, aes(x = Q19))

# Joining data
library(sqldf)
users <- fread('data/users_int.csv')
users <- select(users, -1)
users <- data.frame(users)
names(users)[1] = 'User'
train <- fread('data/train.csv')
train <- data.frame(train)
test <- fread('data/test.csv')
test <- data.frame(test)

joined <- sqldf("SELECT * FROM train JOIN users USING(User)")
write.csv(joined, 'data/joined_train.csv')

joinedTest <- sqldf("SELECT * FROM test JOIN users USING(User)")
write.csv(joinedTest, 'data/joined_test.csv')

# FULL LEFT JOIN
fullJoin <- sqldf("SELECT * FROM train LEFT JOIN users ON train.User = users.RESPID")
write.csv(fullJoin, 'data/joined_train_ALL.csv')

fullJoinTest <- sqldf("SELECT * FROM test LEFT JOIN users ON test.User = users.RESPID")
write.csv(fullJoinTest, 'data/joined_test_ALL.csv')

# Cleaning up words.csv
# Of 86 features, only 25 have less than 10% NA's
words <- read.csv('data/words.csv')
words <- select(words, c(1:4, 9, 17, 24, 26, 28, 36:39, 41:42, 48, 52, 54:55, 57:58, 60, 62, 64, 68, 70, 86))
dummy <- acm.disjonctif(words[c('HEARD_OF', 'OWN_ARTIST_MUSIC')])
nodummy <- select(words, -c(3, 4))
words <- cbind(nodummy, dummy)

write.csv(words, 'data/words_fewer_cols.csv')

upbeatna <- filter(words, Upbeat %nin% c(0, 1))
upbeatnona <- filter(words, Upbeat %in% c(0, 1))
meanUpbeat <- sum(upbeatnona$Upbeat)/nrow(words)
upbeatna <- mutate(upbeatna, Upbeat = meanUpbeat)
words <- rbind(upbeatna, upbeatnona)

youthfulna <- filter(words, Youthful %nin% c(0, 1))
youthfulnona <- filter(words, Youthful %in% c(0, 1))
meanYouthful <- sum(youthfulnona$Youthful)/nrow(words)
youthfulna <- mutate(youthfulna, Youthful = meanYouthful)
words <- rbind(youthfulna, youthfulnona)

catchyna <- filter(words, Catchy %nin% c(0, 1))
catchynona <- filter(words, Catchy %in% c(0, 1))
meanCatchy <- sum(catchynona$Catchy)/nrow(words)
catchyna <- mutate(catchyna, Catchy = meanCatchy)
words <- rbind(catchyna, catchynona)

write.csv(words, 'data/words_noNA.csv')

# Joining train/test and words files on user
words <- fread('data/words_noNA.csv')
words <- select(words, -1)
words <- mutate(words, user_artist = paste(User, Artist, sep = ' '))
train <- fread('data/joined_train_ALL.csv')
train <- select(train, -1)
train <- mutate(train, user_artist = paste(User, Artist, sep = ' '))
test <- fread('data/joined_test_ALL.csv')
test <- select(test, -1)
test <- mutate(test, user_artist = paste(User, Artist, sep = ' '))

full_users_words <- sqldf("SELECT * FROM train LEFT JOIN words ON train.user_artist = words.user_artist")
names(full_users_words)[56] <- 'D1'
names(full_users_words)[57] <- 'D2'
names(full_users_words)[58] <- 'D3'
full_users_words <- select(full_users_words, -c(56:58, 98))
write.csv(full_users_words, 'data/joined_users_words_train.csv')

full_users_words_test <- sqldf("SELECT * FROM test LEFT JOIN words ON test.user_artist = words.user_artist")
names(full_users_words_test)[55] <- 'D1'
names(full_users_words_test)[56] <- 'D2'
names(full_users_words_test)[57] <- 'D3'
full_users_words_test <- select(full_users_words_test, -c(55:57, 97))
write.csv(full_users_words_test, 'data/joined_users_words_test.csv')
