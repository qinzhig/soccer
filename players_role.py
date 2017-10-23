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

    print("**********************team a players list ***************************************")
    print(teamA_players_list)


    teamA_players_FW_attribute = []
    teamA_players_MD_attribute = []
    teamA_players_DF_attribute = []
    teamA_players_GK_attribute = []
    
    teamB_players_FW_attribute = []
    teamB_players_MD_attribute = []
    teamB_players_DF_attribute = []
    teamB_players_GK_attribute = []
    for id in teamA_players_list:
        c = conn.cursor()
        print id
        sql_fw = "select attacking_work_rate,defensive_work_rate,finishing,heading_accuracy,dribbling,curve,ball_control,acceleration,agility,balance,shot_power,jumping,aggression,positioning,penalties from player_attributes where player_api_id = {0}".format(id)
        sql_md = "select crossing,finishing,short_passing,volleys,dribbling,free_kick_accuracy,long_passing,ball_control,sprint_speed,agility,reactions,balance,stamina,long_shots,interceptions,vision from player_attributes where player_api_id = {0}".format(id)
        sql_df = "select attacking_work_rate,defensive_work_rate,heading_accuracy,long_passing,reactions,balance,jumping,strength,positioning,vision,marking,standing_tackle,sliding_tackle from player_attributes where player_api_id = {0}".format(id)
        sql_gk = "select gk_diving,gk_handling,gk_kicking,gk_positioning,gk_positioning from player_attributes where player_api_id = {0}".format(id)

        # print("sql:" + sql)
        for r_FW in c.execute(sql_fw):
            print("*******************forward*******************")
            #print r_FW
            r_FW = list(r_FW)
            try:
            #    r_a[2] = foot_map[r_a[2]]
                r_FW[0] = level_map[r_FW[0]]
                r_FW[1] = level_map[r_FW[1]]
                teamA_players_FW_attribute.append(r_FW)
            except Exception as e:
                pass
        
        for r_MD in c.execute(sql_md):
            print("*******************MD*******************")
            r_MD = list(r_MD)
            try:
                teamA_players_MD_attribute.append(r_MD)
            except Exception as e:
                pass

        for r_DF in c.execute(sql_df):
            print("*******************DF*******************")
            r_DF = list(r_DF)
            try:
                r_DF[0] = level_map[r_DF[0]]
                r_DF[1] = level_map[r_DF[1]]
                teamA_players_DF_attribute.append(r_DF)
            except Exception as e:
                pass

        for r_a_gk in c.execute(sql_gk):
            print("*******************DF*******************")
            r_a_gk = list(r_a_gk)
            try:
                teamA_players_GK_attribute.append(r_a_gk)
            except Exception as e:
                pass
      
    for id in teamB_players_list:
        print id
        sql_fw = "select attacking_work_rate,defensive_work_rate,finishing,heading_accuracy,dribbling,curve,ball_control,acceleration,agility,balance,shot_power,jumping,aggression,positioning,penalties from player_attributes where player_api_id = {0}".format(id)
        sql_md = "select crossing,finishing,short_passing,volleys,dribbling,free_kick_accuracy,long_passing,ball_control,sprint_speed,agility,reactions,balance,stamina,long_shots,interceptions,vision from player_attributes where player_api_id = {0}".format(id)
        sql_df = "select attacking_work_rate,defensive_work_rate,heading_accuracy,long_passing,reactions,balance,jumping,strength,positioning,vision,marking,standing_tackle,sliding_tackle from player_attributes where player_api_id = {0}".format(id)
        sql_gk = "select gk_diving,gk_handling,gk_kicking,gk_positioning,gk_positioning from player_attributes where player_api_id = {0}".format(id)
        # print("sql:" + sql)
        for r_b_fw in c.execute(sql_fw):
            # print r_b
            r_b_fw = list(r_b_fw)
            try:
                #r_b[2] = foot_map[r_b[2]]
                r_b_fw[0] = level_map[r_b_fw[0]]
                r_b_fw[1] = level_map[r_b_fw[1]]
                teamB_players_FW_attribute.append(r_b_fw)
            except Exception as e:
                pass
        for r_b_md in c.execute(sql_md):
            r_b_md = list(r_b_md)
            try:
                teamB_players_MD_attribute.append(r_b_md)
            except Exception as e:
                pass
        for r_b_df in c.execute(sql_df):
            r_b_df = list(r_b_df)
            try:
                r_b_df[0] = level_map[r_b_df[0]]
                r_b_df[1] = level_map[r_b_df[1]]
                teamA_players_DF_attribute.append(r_DF)
            except Exception as e:
                pass
        for r_b_gk in c.execute(sql_gk):
            r_b_gk = list(r_b_gk)
            try:
                teamB_players_GK_attribute.append(r_b_gk)
            except Exception as e:
                pass

    print("**********************teamA*****FW************************************")
    print(teamA_players_FW_attribute)
    print("**********************teamA*****FW************************************")
    print(teamA_players_MD_attribute)
    print(teamA_players_DF_attribute)
    print(teamA_players_GK_attribute)

    print(teamB_players_FW_attribute)
    print(teamB_players_MD_attribute)
    print(teamB_players_DF_attribute)
    print(teamB_players_GK_attribute)

    return teamA_players_FW_attribute, teamA_players_MD_attribute,teamA_players_DF_attribute,teamA_players_GK_attribute,teamB_players_FW_attribute,teamB_players_MD_attribute,teamB_players_DF_attribute,teamB_players_GK_attribute


if __name__ == '__main__':
    a_fw,a_md,a_df,a_gk,b_fw,b_md,b_df,b_gk = get_players_role()
    
    a_fw_array = np.asarray(a_fw)
    print("**********************teamA*****FW********    IN  NP ARRAY  ****************************")
    print(a_fw_array)
    print("**********************teamA*****FW********    IN  NP ARRAY  ****************************")


#####################################################
    a_md_array = np.asarray(a_md)
    temp_list = []
    for w in a_md_array:
        list = []
        for i in w:
            if i != None:
                list = list + [i]
        temp_list = temp_list + [list]

    a_md_array_list = []

    for w in temp_list:
        if w != []:
            a_md_array_list = a_md_array_list + [w]
#####################################################
    a_df_array = np.asarray(a_df)
#####################################################
    a_gk_array = np.asarray(a_gk)
    temp_list_gk = []
    for w in a_gk_array:
        list = []
        for i in w:
            if i != None:
                list = list + [i]
        temp_list_gk = temp_list_gk + [list]
    a_gk_array_list = []
    for w in temp_list_gk:
        if w != []:
            a_gk_array_list = a_gk_array_list + [w]
        

    kmeans_a_fw = KMeans(n_clusters=2, random_state=0).fit(a_fw_array)
    kmeans_a_md = KMeans(n_clusters=2, random_state=0).fit(a_md_array_list)
    kmeans_a_df = KMeans(n_clusters=2, random_state=0).fit(a_df_array)
    kmeans_a_gk = KMeans(n_clusters=2, random_state=0).fit(a_gk_array_list)



    print("teamA")
    print("*****************************FW***********************************")
    print kmeans_a_fw.labels_
    print("*****************************MD***********************************")
    print kmeans_a_md.labels_
    print("*****************************DF***********************************")
    print kmeans_a_df.labels_
    print("*****************************GK***********************************")
    print kmeans_a_gk.labels_





