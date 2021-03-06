#!/usr/bin/python

import json
import sqlite3
from collections import Counter
from flask import Flask
from odds_prediction import predictOdds
from score_prediction import predictScore
from predict_role import predict_role
from gap_prediction import predictGap
from score_prediction import predictScore

app = Flask(__name__, static_url_path='/static')
conn = sqlite3.connect('database.sqlite')


@app.route('/')
def root():
    return app.send_static_file('index.html')


@app.route('/q/<table>')
@app.route('/q/<table>/<key>/<val>')
def query(table, key="", val=""):
    c = conn.cursor()
    sql = "SELECT * FROM %s" % table
    if key and val:
        sql += (" where %s='%s'" % (key, val))
    c.execute(sql)
    return json.dumps(c.fetchall())


@app.route('/team/league/<int:id>')
def team_league(id):
    c = conn.cursor()
    c.execute("select * from team where team_api_id in (SELECT DISTINCT home_team_api_id from match where league_id=%s);" % id)
    return json.dumps(c.fetchall())

def sel_player_team(X, Y):
    sql = "select {0} from match where home_team_api_id = {2} and away_team_api_id = {3} union select {1} from match where home_team_api_id = {3} and away_team_api_id = {2}".format(
        ",".join(map((lambda i: "home_player_%s" % i), range(1, 12))),
        ",".join(map((lambda i: "away_player_%s" % i), range(1, 12))),
        X, Y)
    return sql

@app.route('/player/team/<int:teamX>-<int:teamY>/<Xline>/<Yline>')
def player_team(teamX, teamY, Xline, Yline):
    c = conn.cursor()
    x_line = Xline.split("_")[::-1]
    y_line = Yline.split("_")[::-1]


    ts = [(teamX,teamY),(teamY,teamX)]
    tl = [x_line,y_line]
    tps = []

    for index, t in enumerate(ts):
        sql = sel_player_team(*t)
        print("sql:" + sql)
        c.execute(sql)
        ms = c.fetchall()

        pids = [p for y in ms for p in y]

        print(str(index) + " : " + str(tl[index]))

        c = conn.cursor()
        print("%s raw players: %s" % (t[0],pids))

        cnt = Counter()
        for pid in pids:
            cnt[pid] += 1

        pids = [e[0] for e in cnt.most_common()]
        print("%s 11 players: %s" % (t[0],pids))
        pids = [i for i in pids if i != None]
        print("length : "+str(len(pids)))

        columns = "player_fifa_api_id,player_api_id,date,overall_rating,potential,preferred_foot,attacking_work_rate,defensive_work_rate,crossing,finishing,heading_accuracy,short_passing,volleys,dribbling,curve,free_kick_accuracy,long_passing,ball_control,acceleration,sprint_speed,agility,reactions,balance,shot_power,jumping,stamina,strength,long_shots,aggression,interceptions,positioning,vision,penalties,marking,standing_tackle,sliding_tackle,gk_diving,gk_handling,gk_kicking,gk_positioning,gk_reflexes"
        sql = "select * from Player_Attributes where {0} and {1} and id in (select id from Player_Attributes where player_api_id in ({2}) group by player_api_id having max(date)=date);".format(
            " and ".join(map((lambda i: "%s is not null" %
                            i), columns.split(","))),
            ' preferred_foot in ("left","right") and attacking_work_rate in ("low","medium","high") and defensive_work_rate in ("low","medium","high")',
            ",".join(map(lambda p: str(p), pids)),
        )
        print("predict and pick sql:" + sql)
        c.execute(sql)
        ps = c.fetchall()
        xs = []
        foot = {
            "left": 0,
            "right": 1
        }
        level = {
            "low": 0,
            "medium": 1,
            "high": 2
        }

        pids2 = []
        for p in ps:
            x = list(p)
            x[6] = foot[p[6]]
            x[7] = level[p[7]]
            x[8] = level[p[8]]
            xs.append(x)
            pids2.append(x[2])

        pids = pids2

        print("After SQL number of PIDS : " + str(len(pids2)))
        rs = predict_role(xs)
        print("original rs: " + str(index) +" : " + str(rs)+ ": rs length :" + str(len(rs)))

        ls=[]
        ps=[]
        ATnum = int(tl[index][0])
        MDnum = int(tl[index][1])
        DFnum = int(tl[index][2])
        a, m, d, g = 0, 0, 0, 0
        for index2,i in enumerate(pids):
            if rs[index2] == 'GK' and g < 1:
                ls.append(i)
                ps.append(rs[index2])
                g += 1
            elif rs[index2] == 'AT' and a < ATnum:
                ls.append(i)
                ps.append(rs[index2])
                a += 1
            elif rs[index2] == 'MD' and m < MDnum:
                ls.append(i)
                ps.append(rs[index2])
                m += 1
            elif rs[index2] == 'DF' and d < DFnum:
                ls.append(i)
                ps.append(rs[index2])
                d += 1
        while len(ls) < 11:
            for index3,i2 in enumerate(pids):
                if i2 not in ls:
                    if a < ATnum:
                        ls.append(i2)
                        ps.append('AT')
                        a += 1
                    elif m < MDnum:
                        ls.append(i2)
                        ps.append('MD')
                        m += 1
                    elif d < DFnum:
                        ls.append(i2)
                        ps.append('DF')
                        d += 1

        pids = ls
        rs = ps
        print("predict pids: " + str(pids))
        print("predict rs: " + str(rs))
        sql = "select player_api_id, player_name from Player where player_api_id in ({0});".format(
            ",".join(map(lambda p: str(p), pids)),
            )
        print("pick player sql:" + sql)
        c.execute(sql)
        pds = c.fetchall()
        zs = []
        #print(rs)
        for i in range(11):
            zs.append([pids[i], rs[i]] + [pd[1] for pd in pds if pd[0] == pids[i]])
        tps.append(zs)
    return json.dumps(tps)


@app.route('/predict/<int:teamX>-<int:teamY>')
def predict(teamX, teamY):
    odds = predictOdds(teamX, teamY)
    c = conn.cursor()

    ts = [(teamX,teamY),(teamY,teamX)]
    tps = []
    for t in ts:
        sql = sel_player_team(*t)
        print("sql:" + sql)
        c.execute(sql)
        ms = c.fetchall()
        pids = [p for y in ms for p in y]
        c = conn.cursor()
        print("%s raw players: %s" % (t[0],pids))

        cnt = Counter()
        for pid in pids:
            cnt[pid] += 1

        pids = [e[0] for e in cnt.most_common(11)]
        print("%s 11 players: %s" % (t[0],pids))

        #columns = "player_fifa_api_id,player_api_id,date,overall_rating,potential,preferred_foot,attacking_work_rate,defensive_work_rate,crossing,finishing,heading_accuracy,short_passing,volleys,dribbling,curve,free_kick_accuracy,long_passing,ball_control,acceleration,sprint_speed,agility,reactions,balance,shot_power,jumping,stamina,strength,long_shots,aggression,interceptions,positioning,vision,penalties,marking,standing_tackle,sliding_tackle,gk_diving,gk_handling,gk_kicking,gk_positioning,gk_reflexes"
        columns = "player_api_id,overall_rating"
        sql = "select overall_rating from Player_Attributes where {0} and {1} and id in (select id from Player_Attributes where player_api_id in ({2}) group by player_api_id having max(date)=date);".format(
            " and ".join(map((lambda i: "%s is not null" %
                            i), columns.split(","))),
            ' preferred_foot in ("left","right") and attacking_work_rate in ("low","medium","high") and defensive_work_rate in ("low","medium","high")',
            ",".join(map(lambda p: str(p), pids)),
        )
        print("sql:" + sql)
        c.execute(sql)
        ps = c.fetchall()
        ps = [b[0] for b in ps]
        print("ps:%s" % ps)
        tps.append(ps)

    if teamX == teamY:
        data = {
            "odds":  [0, 1, 0]
        }
    else:
        data = {
            "odds":  odds
        }

    for i in range(0,11 - len(tps[0])):
        tps[0].append(sum(tps[0])/len(tps[0]))

    for i in range(0,11 - len(tps[1])):
        tps[1].append(sum(tps[0])/len(tps[0]))

    data["gap"] = predictGap(odds+tps[0]+tps[1])
    #a=predictGap(odds+tps[0]+tps[1])
    print("return predict"+str(data))
    return json.dumps(data)

@app.route('/match')
def match():
    c = conn.cursor()
    sql = "select player_api_id, overall_rating from Player_Attributes;"
    c.execute(sql)
    rs = c.fetchall()
    d = {}
    for r in rs:
        d[r[0]] = r[1]
    hda = "BWH,BWD,BWA,IWH,IWD,IWA,LBH,LBD,LBA,PSH,PSD,PSA,WHH,WHD,WHA,SJH,SJD,SJA,VCH,VCD,VCA,GBH,GBD,GBA,BSH,BSD,BSA"

    sql = "select home_team_goal-away_team_goal, {0}, {1}, {4} from match where ({2} and {3} and {5});".format(
        ",".join(map((lambda i: "home_player_%s" % i), range(1, 12))),
        ",".join(map((lambda i: "away_player_%s" % i), range(1, 12))),
        " and ".join(
            map((lambda i: "home_player_%s is not null" % i), range(1, 12))),
        " and ".join(
            map((lambda i: "away_player_%s is not null" % i), range(1, 12))),
        hda,
        " and ".join(map((lambda i: "%s is not null" % i), hda.split(","))),
    )
    print("sql:" + sql)
    c.execute(sql)
    ms = c.fetchall()
    xs = []
    for m in ms:
        x = list(m)
        for i in range(1, 23):
            if d[m[i]] is None:
                break
            x[i]= d[m[i]]
        else:
            xs.append(x)
    return json.dumps(xs)


if __name__ == "__main__":
    app.run()
