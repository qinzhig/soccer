import sqlite3
import pandas as pd
from sklearn import svm
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn import linear_model
import numpy as np
from pandas import Series, DataFrame

db_con = sqlite3.connect("database.sqlite")
####################################################################################
#spin League id & Country id both equal to 21518
country_id = '21518'

spain_league_team_id  = pd.read_sql_query("select distinct home_team_api_id from Match where league_id= " + country_id,db_con)
#print(spain_league_team_id)


#search in the Team table to filter out all the teams belong to Spain League
teams = pd.read_sql_query("SELECT team_api_id,team_long_name,team_short_name from Team", db_con)
spain_teams = teams[teams.team_api_id.isin(spain_league_team_id.home_team_api_id)]
#print(spain_teams)

spain_teams_2016 = ['REA','BAR','AMA','SEV','VAL','VIL','SOC','BIL','ESP','BET','LEV','CEL','GET','COR','EIB','MAL','LAS','GRA','SPG','RAY']
####################################################################################
#Retain the match data to fetch out only the essential columns for spain league
matches = pd.read_sql_query("select * from Match where league_id= " + country_id,db_con)

matches = matches.merge(spain_teams,left_on="home_team_api_id",right_on="team_api_id",suffixes=('','_h'))
matches = matches.merge(spain_teams,left_on="away_team_api_id",right_on="team_api_id",suffixes=('','_h'))

#Just filter out the 2015/2016 data for spain team Liga
matches = matches[matches.team_short_name.isin(spain_teams_2016)]
matches = matches[matches.team_short_name_h.isin(spain_teams_2016)]

season_list = ['2015/2016']
matches = matches[matches.season.isin(season_list)]

# B365H,B365D,B365A,
# BWH,BWD,BWA,
# IWH,IWD,IWA,
# LBH,LBD,LBA,
# PSH,PSD,PSA,
# WHH,WHD,WHA,
# SJH,SJD,SJA,-----empty
# VCH,VCD,VCA,
# GBH,GBD,GBA,-----empty
# BSH,BSD,BSA -----empty

#matches = matches[['season','date','home_team_api_id','team_long_name','team_short_name','away_team_api_id',"team_long_name_h",'team_short_name_h','home_team_goal','away_team_goal','B365H', 'B365D' ,'B365A','BWH','BWD','BWA']]
#matches.dropna(inplace=True)
#matches_win = matches[['season','home_team_api_id','team_long_name','team_short_name','away_team_api_id',"team_long_name_h",'team_short_name_h','B365H','BWH','IWH','LBH','PSH','WHH','VCH']]

#Home Team Win Odds Data
matches_win = matches[['season','team_long_name','team_short_name',"team_long_name_h",'team_short_name_h','B365H','BWH','IWH','LBH','PSH','WHH','VCH']]

#Draw Odds Data
matches_draw = matches[['season','team_long_name','team_short_name',"team_long_name_h",'team_short_name_h','B365D','BWD','IWD','LBD','PSD','WHD','VCD']]

#Away Team Win Odds Data
matches_lose = matches[['season','team_long_name','team_short_name',"team_long_name_h",'team_short_name_h','B365A','BWA','IWA','LBA','PSA','WHA','VCA']]

matches_win=matches_win.dropna(axis=0,how='any')
matches_draw=matches_draw.dropna(axis=0,how='any')
matches_lose=matches_lose.dropna(axis=0,how='any')

#matches_win = matches[['season','team_short_name','team_short_name_h','B365H','BWH','IWH','LBH','PSH','WHH','VCH']]
#print(matches_win.head(50))

matches_win = matches_win.assign(mean_win = matches_win.mean(axis=1), mean_draw = matches_draw.mean(axis=1),mean_lose = matches_lose.mean(axis=1))
#matches_draw = matches_draw.assign(mean_draw = matches_draw.mean(axis=1))
#matches_lose = matches_lose.assign(mean_lose = matches_lose.mean(axis=1))
#print(matches_win.head(20))
####################################################################################
#Retrieval the team property data like shotting,defence...
teams_prop = pd.read_sql_query("SELECT team_api_id, date, chanceCreationShooting, defencePressure from Team_Attributes ", db_con)
teams_prop = teams_prop[teams_prop.team_api_id.isin(matches.home_team_api_id)]
#print(teams_prop.head(20))

date_list =['2015-09-10 00:00:00']
teams_prop = teams_prop[teams_prop.date.isin(date_list)]

teams_prop = teams_prop.merge(spain_teams,left_on="team_api_id",right_on="team_api_id",suffixes=('','_t'))
#teams_prop = teams_prop[['team_api_id','team_long_name','team_short_name','chanceCreationShooting','defencePressure']]
teams_prop = teams_prop[['team_short_name','chanceCreationShooting','defencePressure']]

teams_prop.rename(columns={'chanceCreationShooting':'offence', 'defencePressure':'defence'}, inplace = True)
#print(teams_prop.head(20))
####################################################################################
#Data Normalization
matches_win = matches_win.merge(teams_prop,left_on="team_short_name",right_on="team_short_name",suffixes=('','_t'))
matches_win = matches_win.merge(teams_prop,left_on="team_short_name_h",right_on="team_short_name",suffixes=('','_t'))

#matches_win = matches_win[['team_long_name','team_short_name','team_long_name_h','team_short_name_h','offence','defence','offence_t','defence_t','mean']]
#print(matches_win.head(20))

####################################################################################
#Data normalization to remap the data range to 0-1 by using function x - min / max -min

power_data = matches_win[['offence','defence','offence_t','defence_t']]

func1 = lambda x: (x - x.min())/(x.max() - x.min())
power_data = power_data.apply(func1)

odds_data_win = matches_win[['mean_win']]
odds_data_draw = matches_win[['mean_draw']]
odds_data_lose = matches_win[['mean_lose']]

merged_data = power_data.assign(mean_win = odds_data_win,mean_draw = odds_data_draw,mean_lose = odds_data_lose)

#As the offence/defence (max-min) = 30, so we need to make sure 1/30 = 0.033 precision for most the data.
#Apply format formula as %.3f for data matrix
format1 = lambda x: '%.3f' % x
merged_data = merged_data.applymap(format1)

#print(merged_data.head(40))

####################################################################################
#Shuffle and Slice Data for feeding the model
merged_data = shuffle(merged_data)

X = merged_data[['offence','defence','offence_t','defence_t']]
y_win = merged_data[['mean_win']]
y_draw = merged_data[['mean_draw']]
y_lose = merged_data[['mean_lose']]

X = X.copy()

X['power_sum'] = pd.to_numeric(X['offence']) + pd.to_numeric(X['defence'])
X['power_sum_t'] = pd.to_numeric(X['offence_t']) + pd.to_numeric(X['defence_t'])

#X['power_gap'] = pd.to_numeric(X['power_sum']) - pd.to_numeric(X['power_sum_t'])
#X['offence_gap'] = pd.to_numeric(X['offence']) - pd.to_numeric(X['offence_t'])
#X['defence_gap'] = pd.to_numeric(X['defence']) - pd.to_numeric(X['defence_t'])

#X = X[['offence_gap','defence_gap']]
#X = X[['power_sum','power_sum_t']] #best
#X = X[['power_sum','power_sum_t','offence_gap','defence_gap']]
#X = X[['power_sum','power_sum_t','power_gap']]
X = X[['power_sum','power_sum_t']]

#print (X)

X_train_win, X_test_win, y_train_win, y_test_win = train_test_split(X, y_win, test_size=0.1)

X_train_draw, X_test_draw, y_train_draw, y_test_draw = train_test_split(X, y_draw, test_size=0.1)

X_train_lose, X_test_lose, y_train_lose, y_test_lose = train_test_split(X, y_lose, test_size=0.1)

####################################################################################
# Prediction accuracy caculation Function for the test dataset
def result_accuracy(result,var):
    count = 0
    len = 0
    for num in result:
        len = len + 1
        if abs(num) <= var:
            count = count +1

    count=round(count,3)
    len=round(len,3)

    return (count/len)
####################################################################################
# Using SVM to build and test the prediction model.

clf = svm.SVR()

clf.fit(X_train_win, y_train_win.values.ravel())
y_test_predict_win = clf.predict(X_test_win)

clf.fit(X_train_draw, y_train_draw.values.ravel())
y_test_predict_draw = clf.predict(X_test_draw)

clf.fit(X_train_lose, y_train_lose.values.ravel())
y_test_predict_lose = clf.predict(X_test_lose)


####################################################################################
#Using Linear Regression
#model = linear_model.LinearRegression()
#model.fit(X_train,y_train.values.ravel())
#y_test_predict = model.predict(X_test)

############################################################

##########################################################
y_test_win = y_test_win.astype(float).fillna(0.000)
y_gap_win = y_test_predict_win - y_test_win.values.ravel()

y_test_draw = y_test_draw.astype(float).fillna(0.000)
y_gap_draw = y_test_predict_draw - y_test_draw.values.ravel()

y_test_lose = y_test_lose.astype(float).fillna(0.000)
y_gap_lose = y_test_predict_lose - y_test_lose.values.ravel()
#print(result_array)

print("SVM Win Accuracy = %.3f" % result_accuracy(y_gap_win, 0.4))
print("SVM Draw Accuracy = %.3f" % result_accuracy(y_gap_draw, 0.6))
print("SVM Lose Accuracy = %.3f" % result_accuracy(y_gap_lose, 1.2))
#print(result_accuracy(y_gap))
##########################################################





