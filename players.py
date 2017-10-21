from matchHistory import getMatchHistory

def getplayers(teamX, teamY):

    reponse = getMatchHistory(teamX, teamY)

    sqllist = {}
    Xplayers = []
    Yplayers = []
    mlist = []

    for row in reponse:
        player = []
        if (row[2] - row[3]) < 0:
            winner = row[1]
            for i in range(4, 16):
                player.append(row[i])
        elif (row[2] - row[3]) > 0:
            winner = row[0]
            for i in range(16, 27):
                player.append(row[i])
        else:
            winner = 0

        if winner == teamX:
            Xplayers.extend(player)

        elif winner == teamY:
            Yplayers.extend(player)

        ob = {}
        ob["gameid"] = row[26]
        ob["winner"] = winner
        ob["player"] = player
        mlist.append(ob)

    Xplayers = list(set(Xplayers))
    Yplayers = list(set(Yplayers))
    sqllist["Xplayers"] = Xplayers
    sqllist["Yplayers"] = Yplayers
    sqllist["matchList"] = mlist
    print(len(Xplayers))
    print(len(Yplayers))
    print(len(sqllist["matchList"]))
    return sqllist