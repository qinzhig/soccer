# 1.Setup Application

    git clone https://github.com/huazhihao/soccer && cd soccer
    pip install -r requirement.txt
    FLASK_APP=soccer.py flask run

# 2.Setup Database

    Download [soccer.zip](https://www.kaggle.com/hugomathien/soccer/data) and unzip to ./database.sqlite under this repo working directory.

# 3.How to use this application
    The default application homepage should be [Soccer Prediction Machine](http://127.0.0.1:5000) after Step1 and Step2 is configured successfully.
    
    Then you can choose the League: **Spanish LIGA**, for home team and away team
    
    Then you can choose the current LIGA teams like below:
	8315	Athletic Club de Bilbao
	9906	Atletico Madrid
	8634	FC Barcelona
	9910	RC Celta de Vigo
	9783	RC Deportivo de La Coruna
	8372	SD Eibar
	8558	RCD Espanyol
	8305	Getafe CF
	7878	Granada CF
	8306	UD Las Palmas
	8581	Levante UD
	9864	Malaga CF
	8370	Rayo Vallecano
	8603	Real Betis Balompie
	8633	Real Madrid CF
	8560	Real Sociedad
	8302	Sevilla FC
	9869	Real Sporting de Gijon
	10267	Valencia CF
	10205	Villarreal CF

    And then,you can also choose the Line-Up for the 2 teams.

    Finally,kick predict button to get the result 

# Query APIs

## Generic queries

    curl http://127.0.0.1:5000/q/league # all leagues
    curl http://127.0.0.1:5000/q/league/country_id/1729 # league "England Premier League"
    curl http://127.0.0.1:5000/q/team/team_api_id/8455 # team Chelsea

## Ad hoc queries

    curl http://127.0.0.1:5000/team/league/1729 # all teams under "England Premier League"
    curl http://127.0.0.1:5000/player/team/8455-10260 # all players attended the match between Chelsea and Manchester United
