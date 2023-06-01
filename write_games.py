import pymysql
import pandas as pd
import mysql.connector
from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder

columns = ['SEASON_ID', 'TEAM_ID', 'TEAM_ABBREVIATION', 'TEAM_NAME', 'GAME_ID',
       'GAME_DATE', 'MATCHUP', 'WL']
teams_df = []
for team in teams.get_teams():
    team_id = team["id"]
    team_games = leaguegamefinder.LeagueGameFinder(team_id_nullable = team_id)
    team_df = team_games.get_data_frames()[0]
    team_df = team_df[columns]
    filt = team_df["GAME_DATE"] > "2000-00-00"
    team_df = team_df[filt]
    teams_df.append(team_df)

teams_df = pd.concat(teams_df,axis = 0)

conn = pymysql.connect(
    host = "mydemodb.c6ttcyoyckbo.us-east-2.rds.amazonaws.com",
    user = "admin",
    password = "mynbaproject"
)
cursor = conn.cursor()

cursor.execute("use NBA")

['SEASON_ID', 'TEAM_ID', 'TEAM_ABBREVIATION', 'TEAM_NAME', 'GAME_ID',
       'GAME_DATE', 'MATCHUP', 'WL']

sql = '''
create table GAMES(
    SEASON_ID varchar(20),
    TEAM_ID varchar(20),
    TEAM_ABBREVIATION varchar(20),
    TEAM_NAME varchar(20),
    GAME_ID varchar(20),
    GAME_DATE varchar(20),
    MATCHUP varchar(20),
    WL varchar(1)
)
'''
cursor.execute(sql)

for indx,row in teams_df.iterrows():
    sql = "insert into GAMES values('%s','%s','%s','%s','%s','%s','%s','%s')"%tuple(val for val in row.tolist())
    cursor.execute(sql)

cursor.connection.commit()
