import sqlite3
import pandas as pd
from sklearn import svm
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn import linear_model
import numpy as np
from pandas import Series, DataFrame


def getOddsDataForSpanish():

    db_con = sqlite3.connect("database.sqlite")
    # spin League id & Country id both equal to 21518
    country_id = '21518'
    spain_league_team_id = pd.read_sql_query("select distinct home_team_api_id from Match where league_id= " + country_id,db_con)

    # search in the Team table to filter out all the teams belong to Spain League
    teams = pd.read_sql_query("SELECT team_api_id,team_long_name,team_short_name from Team", db_con)
    spain_teams = teams[teams.team_api_id.isin(spain_league_team_id.home_team_api_id)]
    # print(spain_teams)

    spain_teams_2016 = ['REA', 'BAR', 'AMA', 'SEV', 'VAL', 'VIL', 'SOC', 'BIL', 'ESP', 'BET', 'LEV', 'CEL', 'GET', 'COR','EIB', 'MAL', 'LAS', 'GRA', 'SPG', 'RAY']


    # Retain the match data to fetch out only the essential columns for spain league
    matches = pd.read_sql_query("select * from Match where league_id= " + country_id, db_con)
    matches = matches.merge(spain_teams, left_on="home_team_api_id", right_on="team_api_id", suffixes=('', '_h'))
    matches = matches.merge(spain_teams, left_on="away_team_api_id", right_on="team_api_id", suffixes=('', '_h'))

    # Just filter out the 2015/2016 data for spain team Liga
    matches = matches[matches.team_short_name.isin(spain_teams_2016)]
    matches = matches[matches.team_short_name_h.isin(spain_teams_2016)]

    season_list = ['2015/2016']
    matches = matches[matches.season.isin(season_list)]

    #Gambling Company Odds data for Spanish League
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

    # Home Team Win Odds Data
    matches_win = matches[['season', 'team_long_name', 'team_short_name', "team_long_name_h", 'team_short_name_h', 'B365H', 'BWH', 'IWH','LBH', 'PSH', 'WHH', 'VCH']]
    # Draw Odds Data
    matches_draw = matches[['season', 'team_long_name', 'team_short_name', "team_long_name_h", 'team_short_name_h', 'B365D', 'BWD', 'IWD','LBD', 'PSD', 'WHD', 'VCD']]
    # Away Team Win Odds Data
    matches_lose = matches[['season', 'team_long_name', 'team_short_name', "team_long_name_h", 'team_short_name_h', 'B365A', 'BWA', 'IWA','LBA', 'PSA', 'WHA', 'VCA']]

    #Remove any line with un-complete data
    matches_win = matches_win.dropna(axis=0, how='any')
    matches_draw = matches_draw.dropna(axis=0, how='any')
    matches_lose = matches_lose.dropna(axis=0, how='any')

    matches_win = matches_win.assign(mean_win=matches_win.mean(axis=1), mean_draw=matches_draw.mean(axis=1),mean_lose=matches_lose.mean(axis=1))

    # Retrieval the team property data like shotting,defence...
    teams_prop = pd.read_sql_query("SELECT team_api_id, date,buildUpPlaySpeed,chanceCreationPassing,chanceCreationCrossing,chanceCreationShooting, defencePressure,defenceAggression, defenceTeamWidth from Team_Attributes ", db_con)
    teams_prop = teams_prop[teams_prop.team_api_id.isin(matches.home_team_api_id)]

    date_list = ['2015-09-10 00:00:00']
    teams_prop = teams_prop[teams_prop.date.isin(date_list)]

    teams_prop = teams_prop.merge(spain_teams, left_on="team_api_id", right_on="team_api_id", suffixes=('', '_t'))
    teams_prop = teams_prop[['team_short_name','buildUpPlaySpeed','chanceCreationPassing','chanceCreationCrossing','chanceCreationShooting', 'defencePressure','defenceAggression','defenceTeamWidth']]

    teams_prop['power'] = teams_prop['buildUpPlaySpeed'] +teams_prop['chanceCreationShooting'] + teams_prop['defenceAggression']

    #Data concating
    matches_win = matches_win.merge(teams_prop, left_on="team_short_name", right_on="team_short_name", suffixes=('', '_t'))
    matches_win = matches_win.merge(teams_prop, left_on="team_short_name_h", right_on="team_short_name",suffixes=('', '_t'))

    # Data normalization to remap the data range to 0-1 by using function x - min / max -min
    power_data = matches_win[['power','power_t']]

    func1 = lambda x: (x - x.min()) / (x.max() - x.min())
    power_data = power_data.apply(func1)

    odds_data_win = matches_win[['mean_win']]
    odds_data_draw = matches_win[['mean_draw']]
    odds_data_lose = matches_win[['mean_lose']]
    merged_data = power_data.assign(mean_win=odds_data_win, mean_draw=odds_data_draw, mean_lose=odds_data_lose)

    # As the offence/defence (max-min) = 30, so we need to make sure 1/30 = 0.033 precision for most the data.
    # Apply format formula as %.3f for data matrix
    format1 = lambda x: '%.3f' % x
    merged_data = merged_data.applymap(format1)

    return merged_data
