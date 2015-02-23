library(Hmisc)
library(data.table)
library(dplyr)
library(lubridate)
library(stringi)
library(stringr)
library(doParallel)
library(caret)

setwd('/Users/Aluminum/Documents/Machine Learning/Project')
train <- read.csv('train.csv')
users <- read.csv('users.csv')
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