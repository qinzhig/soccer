# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 16:06:32 2017

@author: HP
"""
import sqlite3

def getMatchHistory(teamX, teamY):
    conn = sqlite3.connect('database.sqlite')

    c = conn.cursor()
    sql = "select home_team_api_id, away_team_api_id, home_team_goal, away_team_goal, {0}, {1}, match_api_id from match where (home_team_api_id = {2} and away_team_api_id = {3}) or (home_team_api_id = {3} and away_team_api_id = {2});".format(
        ",".join(map((lambda i: "home_player_%s" % i), range(1, 12))),
        ",".join(map((lambda i: "away_player_%s" % i), range(1, 12))),
        teamX, teamY)
    print("sql:" + sql)

    return c.execute(sql)
