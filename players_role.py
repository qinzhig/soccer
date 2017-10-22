# coding: utf-8
import numpy as np
import matplotlib.pyplot as plt
import sqlite3

from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
from sklearn import datasets

from players import getplayers

foot_map = {
    "left": 0,
    "right": 1
}

level_map = {
    "low": 0,
    "medium": 1,
    "high": 2
}


def get_players_role():
    teamX=8455
    teamY=10260
    conn = sqlite3.connect('database.sqlite')
    players_list = getplayers(teamX,teamY)

    teamA_players_list = players_list["Xplayers"]
    teamB_players_list = players_list["Yplayers"]
    teamA_players_attribute = []
    teamB_players_attribute = []

    for id in teamA_players_list:
        c = conn.cursor()
        print id
        sql = "select overall_rating,potential,preferred_foot,attacking_work_rate,defensive_work_rate,crossing,finishing,heading_accuracy,short_passing,volleys,dribbling,curve,free_kick_accuracy,long_passing,ball_control,acceleration,sprint_speed,agility,reactions,balance,shot_power,jumping,stamina,strength,long_shots,aggression,interceptions,positioning,vision,penalties,marking,standing_tackle,sliding_tackle from player_attributes where player_api_id = {0}".format(id)
        # print("sql:" + sql)
        for r_a in c.execute(sql):
            # print r_a
            r_a = list(r_a)
            try:
                r_a[2] = foot_map[r_a[2]]
                r_a[3] = level_map[r_a[3]]
                r_a[4] = level_map[r_a[4]]
                teamA_players_attribute.append(r_a)
            except Exception as e:
                pass

    for id in teamB_players_list:
        print id
        sql = "select overall_rating,potential,preferred_foot,attacking_work_rate,defensive_work_rate,crossing,finishing,heading_accuracy,short_passing,volleys,dribbling,curve,free_kick_accuracy,long_passing,ball_control,acceleration,sprint_speed,agility,reactions,balance,shot_power,jumping,stamina,strength,long_shots,aggression,interceptions,positioning,vision,penalties,marking,standing_tackle,sliding_tackle from player_attributes where player_api_id = {0}".format(id)
        # print("sql:" + sql)
        for r_b in c.execute(sql):
            # print r_b
            r_b = list(r_b)
            try:
                r_b[2] = foot_map[r_b[2]]
                r_b[3] = level_map[r_b[3]]
                r_b[4] = level_map[r_b[4]]
                teamB_players_attribute.append(r_b)
            except Exception as e:
                pass

    print(teamA_players_attribute)

    print(teamB_players_attribute)
    return teamA_players_attribute, teamA_players_attribute


if __name__ == '__main__':
    a, b = get_players_role()
    a_array = np.asarray(a)
    kmeans_a = KMeans(n_clusters=3, random_state=0).fit(a_array)
    print kmeans_a.labels_

    b_array = np.asarray(b)
    kmeans_b = KMeans(n_clusters=3, random_state=0).fit(b_array)
    print kmeans_b.labels_

