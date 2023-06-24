from nba_api.stats.static import teams,players
from nba_api.stats.endpoints import leaguegamefinder
import pandas as pd

class NBA_ApiHelper:
    name_to_id = {}
    def get_team_id(team_name):
        if not NBA_ApiHelper.name_to_id:
            for team in teams.get_teams():
                NBA_ApiHelper.name_to_id[team["full_name"]] = team["id"]
        return NBA_ApiHelper.name_to_id[team_name]
    
    id_to_name = {}
    def get_team_name(team_id):
        if not NBA_ApiHelper.id_to_name:
            for team in teams.get_teams():
                NBA_ApiHelper.id_to_name[team["id"]] = team["full_name"]
        return NBA_ApiHelper.id_to_name[team_id]

 

    
