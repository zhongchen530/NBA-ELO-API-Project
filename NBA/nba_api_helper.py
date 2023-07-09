from nba_api.stats.static import teams,players
from nba_api.stats.endpoints import leaguegamefinder
import schedule

class PlayerInfo:
    id_to_info = {}
    name_to_info = {}


class TeamInfo:
    id_to_info = {}
    name_to_info = {}

def update():
    for team in teams.get_teams():
        TeamInfo.id_to_info[team["id"]] = team
        TeamInfo.name_to_info[team["full name"]] = team
    for player in players.get_players():
        PlayerInfo.id_to_info[player["id"]] = player
        PlayerInfo.name_to_info[player["full name"]] = player
        
update()
schedule.every().day.at("00:00").do(update)