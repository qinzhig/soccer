#!/usr/bin/python

import json
import sqlite3
from flask import Flask
from odds_prediction import predictOdds

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


@app.route('/player/team/<int:teamX>-<int:teamY>')
def player_team(teamX, teamY):
    c = conn.cursor()
    sql = "select {0}, {1} from match where (home_team_api_id = {2} and away_team_api_id = {3}) or (home_team_api_id = {3} and away_team_api_id = {2});".format(
        ",".join(map((lambda i: "home_player_%s" % i), range(1, 12))),
        ",".join(map((lambda i: "away_player_%s" % i), range(1, 12))),
        teamX, teamY)
    print("sql:" + sql)
    c.execute(sql)
    ms = c.fetchall()
    ps = [p for y in ms for p in y]
    c = conn.cursor()
    print ps
    columns = "player_fifa_api_id,player_api_id,date,overall_rating,potential,preferred_foot,attacking_work_rate,defensive_work_rate,crossing,finishing,heading_accuracy,short_passing,volleys,dribbling,curve,free_kick_accuracy,long_passing,ball_control,acceleration,sprint_speed,agility,reactions,balance,shot_power,jumping,stamina,strength,long_shots,aggression,interceptions,positioning,vision,penalties,marking,standing_tackle,sliding_tackle,gk_diving,gk_handling,gk_kicking,gk_positioning,gk_reflexes"
    sql = "select * from Player_Attributes where {0} and {1} and id in (select id from Player_Attributes where player_api_id in ({2}) group by player_api_id having max(date)=date);".format(
        " and ".join(map((lambda i: "%s is not null" %
                          i), columns.split(","))),
        ' preferred_foot in ("left","right") and attacking_work_rate in ("low","medium","high") and defensive_work_rate in ("low","medium","high")',
        ",".join(map(lambda p: str(p), ps)),
    )
    print("sql:" + sql)
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
    for p in ps:
        x = list(p)
        x[6] = foot[p[6]]
        x[7] = level[p[7]]
        x[8] = level[p[8]]
        xs.append(x)
    return json.dumps(xs)


@app.route('/predict/<int:teamX>-<int:teamY>')
def predict(teamX, teamY):
    if teamX == teamY:
        data = {
            "score":  [0, 1, 0]
        }
    else:
        data = {
            "score":  predictOdds(teamX, teamY)
        }
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
