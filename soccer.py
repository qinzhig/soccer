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
    return json.dumps(c.fetchall())


@app.route('/predict/<int:teamX>-<int:teamY>')
def predict(teamX, teamY):
    if teamX == teamY:
        data = {
            "score":  [0, 1, 0]
        }
    else:
        data = {
            "score":  predictOdds(teamX,teamY)
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
        " and ".join(map((lambda i: "home_player_%s is not null" % i), range(1, 12))),
        " and ".join(map((lambda i: "away_player_%s is not null" % i), range(1, 12))),
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
            x.append(d[m[i]])
        else:
            xs.append(x)
    return json.dumps(xs)


if __name__ == "__main__":
    app.run()
