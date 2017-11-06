function ddl(rs, k, v) {
    var html = []
    for (var i = 0; i < rs.length; i++) {
        html.push("<option value='" + rs[i][k] + "'>" + rs[i][v] + "</option>")
    }
    return html.join("")
}
function sel(league, target) {
    $.getJSON("/team/league/" + league, function (teams) {
        $("#ddl_team_" + target).html(ddl(teams, 1, 3))
    })
}

function clean(){
    $("#btn_predict").hide()
    $("#score").show()

    $("#win").html("")
    $("#draw").html("")
    $("#lose").html("")
}

$(function () {
    $.getJSON("/q/league", function (leagues) {
        $("#ddl_league_home").html(ddl(leagues, 0, 2)).change(function () {
            sel(this.value, "home")
        })
        sel(1, "home")
        $("#ddl_league_away").html(ddl(leagues, 0, 2)).change(function () {
            sel(this.value, "away")
        })
        sel(1, "away")
    })
    $("#btn_predict").click(function () {
        var home = $("#ddl_team_home").val()
        var away = $("#ddl_team_away").val()

        var home_lineup = $("#ddl_lineup_home").val()
        var away_lineup = $("#ddl_lineup_away").val()


        clean()

        $.getJSON("/predict/" + home + "-" + away, function (data) {
            $("#win").html(data.odds[0].toFixed(2))
            $("#draw").html(data.odds[1].toFixed(2))
            $("#lose").html(data.odds[2].toFixed(2))
        })

        $.getJSON("/player/team/" + home + "-" + away + "/" + home_lineup + "/" + away_lineup, function (data) {
            html = []
            var sd = {
                AT:1,
                MD:2,
                DF:3,
                GK:4
            }
            function s(x,y){
                return sd[x[1]] - sd[y[1]]
            }
            data[0]=data[0].sort(s)
            data[1]=data[1].sort(s)
            var fd = {
                AT:"CF",
                MD:"MF",
                DF:"BF",
                GK:"GK"
            }
            for (var i = 0; i < 11; i++) {
                html.push("<tr><td>"+fd[data[0][i][1]]+" : "+data[0][i][2]+"</td><td>"+fd[data[1][i][1]]+" : "+data[1][i][2]+"</td></tr>")
            }
            $("#tab_players").html(html.join(""))
        })
    })
    $("#score").click(function () {
        $("#score").hide()
        $("#btn_predict").show()
    })
})