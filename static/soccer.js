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

        $("#btn_predict").hide()
        $.getJSON("/predict/" + home + "-" + away, function (data) {
            $("#h1_score").show(data.score)
        })

    })
    $("#h1_score").click(function () {
        $("#h1_score").hide()
        $("#btn_predict").show()
    })
})