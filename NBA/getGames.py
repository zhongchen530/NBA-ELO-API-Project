from nba_api.stats.static import teams,players
from nba_api.stats.endpoints import leaguegamefinder
import pandas as pd

team_columns = ['TEAM_ID', 'GAME_ID',
       'GAME_DATE', 'MATCHUP', 'WL']

name_to_id = {}
def get_team_name(team_name):
    if not name_to_id:
        for team in teams.get_teams():
            name_to_id[team["full_name"]] = team["id"]
    return name_to_id[team_name]

id_to_name = {}
def get_team_name(team_id):
    if not id_to_name:
        for team in teams.get_teams():
            id_to_name[team["id"]] = team["full_name"]
    print(id_to_name,"heyheyheyheyhey")
    return id_to_name[team_id]

def get_team_games(date_range):
    if len(date_range) != 2:
        raise Exception("Expected date_range with length 2,%s given"%len(date_range))
        
    start,end = date_range
    teams_df = []
    
    for team in teams.get_teams():
        team_id = team["id"]
        team_games = leaguegamefinder.LeagueGameFinder(team_id_nullable = team_id)
        team_df = team_games.get_data_frames()[0]
        team_df = team_df[team_columns]
        filt = (start <= team_df["GAME_DATE"]) & (team_df["GAME_DATE"] < end)
        team_df = team_df[filt]
        teams_df.append(team_df)

    teams_df = pd.concat(teams_df,axis = 0)
    
    df1 = teams_df[["GAME_ID","TEAM_ID","GAME_DATE","WL"]]
    df2 = teams_df[["TEAM_ID","GAME_ID"]]
    merged = pd.merge(df1,df2,on = "GAME_ID")
    merged = merged[merged["TEAM_ID_x"] != merged["TEAM_ID_y"]]
    merged.drop_duplicates(subset = "GAME_ID",inplace = True)
    merged = merged.dropna()
    print(merged)
    print("Data retrived sucessfully")
    return merged

def get_player_size():
    return len(players.get_players())

def get_player_games():
    pass
    