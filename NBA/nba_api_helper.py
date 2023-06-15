from nba_api.stats.static import teams,players
from nba_api.stats.endpoints import leaguegamefinder
import pandas as pd

class NBA_ApiHelper:
    team_columns = ['TEAM_ID', 'GAME_ID',
       'GAME_DATE', 'MATCHUP', 'WL']
    
    player_columns = ['PLAYER_ID', 'GAME_ID',
       'GAME_DATE', 'MATCHUP', 'WL']
    
    name_to_id = {}
    def get_team_id(team_name):
        if not name_to_id:
            for team in teams.get_teams():
                name_to_id[team["full_name"]] = team["id"]
        return name_to_id[team_name]
    
    id_to_name = {}
    def get_team_name(team_id):
        if not id_to_name:
            for team in teams.get_teams():
                id_to_name[team["id"]] = team["full_name"]
        return id_to_name[team_id]
    
    def get_team_games(date_from):
        teams_df = []
        
        for team in teams.get_teams():
            team_id = team["id"]
            team_games = leaguegamefinder.LeagueGameFinder(team_id_nullable = team_id,date_from_nullable = date_from)
            team_df = team_games.get_data_frames()[0]
            team_df = team_df[team_columns]
            teams_df.append(team_df)

        return pd.concat(teams_df,axis = 0)

    
