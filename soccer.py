#!/usr/bin/python

import json
import sqlite3
from flask import Flask

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
        ",".join(map((lambda i: "home_player_%s" % i), range(1, 11))),
        ",".join(map((lambda i: "away_player_%s" % i), range(1, 11))),
        teamX, teamY)
    print("sql:" + sql)
    c.execute(sql)
    return json.dumps(c.fetchall())

if __name__ == "__main__":
    app.run()
    


