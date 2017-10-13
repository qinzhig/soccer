function ddl(rs, k, v){
    var html = []
    for (var i = 0; i < rs.length; i++) {
        html.push("<option value='"+rs[i][k]+"'>"+rs[i][v]+"</option>")
    }
    return html.join("")
}
function sel(league,target){
    $.getJSON("/team/league/"+league, function( teams ) {
        $("#ddl_team_"+target).html(ddl(teams, 0, 1))
    })
}

$(function(){
    $.getJSON("/q/league", function( leagues ) {
        $("#ddl_league_home").html(ddl(leagues, 0, 2)).change(function(){
            sel(this.value,"home")
        })
        sel(1,"home")
        $("#ddl_league_away").html(ddl(leagues, 0, 2)).change(function(){
            sel(this.value,"away")
        })
        sel(1,"away")
    })
})