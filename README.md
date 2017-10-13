# Setup

    git clone https://github.com/huazhihao/soccer && cd soccer
    pip install -r requirement.txt
    FLASK_APP=soccer.py flask run

# Database

Download [soccer.zip](https://www.kaggle.com/hugomathien/soccer/data) and unzip to ./database.sqlite under this repo working directory.

# Query

    curl http://127.0.0.1:5000/q/league
    curl http://127.0.0.1:5000/q/league/country_id/1729
    curl http://127.0.0.1:5000/team/league/1729