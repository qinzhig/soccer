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
    c.execute("SELECT id FROM league")
    leagues = c.fetchall()
    i = 0
    next = 0
    for l in leagues:
        if id == l[0]:
            print i, len(leagues)
            if i < len(leagues) - 1:
                next = leagues[i + 1][0]
            else:
                next = 999999
            break
        i+=1
    if next == 0:
        json.dumps([])

    c.execute("select id, team_long_name from team where id>=:min and id<:max", {"min": id, "max": next})
    return json.dumps(c.fetchall())
