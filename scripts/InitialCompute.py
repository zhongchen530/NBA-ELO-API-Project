
from NBA.models import *
from nba_api.stats.static import teams,players
from nba_api.stats.endpoints import leaguegamefinder,playergamelog,playergamelogs
from NBA.name_enums import DfColumnNames,TableColumnNames
import datetime
import time
from NBA.nba_api_helper import NBA_ApiHelper
from NBA.reformat import reformat

def elo_diff(elo1,elo2,wl):
    p1_win = 1/(1+10**((elo2-elo1)/400))
    if wl == "W":
        score = 1
    elif wl == "L":
        score = 0
    elif wl == "T":
        score = 0.5
    return 32*(score - p1_win)

def get_seasons_list():
    return [f"20{str(i).zfill(2)}-{str(i+1).zfill(2)}" for i in range(23)]

def convert_date(date_str):
    return datetime.datetime.strptime(date_str,'%Y-%m-%d').date()

class ComputeTeams:
    def write_games():
        teams_df = NBA_ApiHelper.get_team_games(date_from = "2000-00-00")
        teams_df = reformat(teams_df,"TEAM_ID")
        for indx,row in teams_df.iterrows():
            object = Game(*(row.tolist()))
            object.save()

    def write_team_elo():
        sort_by = "-"+TableColumnNames.GAME_DATE.value
        games = Game.objects.order_by(sort_by)
        for indx,game in enumerate(games):
            try: 
                team1 = CurrentTeamElo.objects.get(pk = game.team_id)
            except:
                team1 = CurrentTeamElo(game.team_id,1000)

            try:
                team2 = CurrentTeamElo.objects.get(pk = game.opponent_id)
            except:
                team2 = CurrentTeamElo(game.opponent_id,1000)

            diff = elo_diff(team1.elo,team2.elo,game.wl)
            team1.elo += diff
            team2.elo -= diff
            team1.save()
            team2.save()

            helo1 = HistoricalTeamElo(indx,team1.team_id,game.game_date,team1.elo)
            helo2 = HistoricalTeamElo(indx,team2.team_id,game.game_date,team2.elo)
            helo1.save()
            helo2.save()

class ComputePlayers:
    def write_player_games():
        seasons = get_seasons_list()
        for season in seasons:
            ComputePlayers.write_season_playergamelogs(season)

    def write_season_playergamelogs(season):
        player_id_name = DfColumnNames.PLAYER_ID.value
        game_id_name = DfColumnNames.GAME_ID.value
        wl_name =  DfColumnNames.WL.value
        
        season_game_logs = playergamelogs.PlayerGameLogs(season_nullable=season)
        df = season_game_logs.get_data_frames()[0]
        print(df.columns)
        for indx,game in df.iterrows():
            object = PlayerGame(player_id = game[player_id_name],game_id = game[game_id_name],wl = game[wl_name])
            object.save()

    def write_player_elo():
        today = datetime.date.today()
        games = Game.objects.order_by("game_date")
        for indx,game in enumerate(games):
            players_list = PlayerGame.objects.filter(game_id = game.game_id)
            if len(players_list) == 0:
                continue
            w_team_elo = 0
            l_team_elo = 0
            w_team_nums = 0
            l_team_nums = 0

            for player in players_list:
                try: 
                    player_elo = CurrentPlayerElo.objects.get(pk = player.player_id)
                except:
                    player_elo = CurrentPlayerElo(player.player_id,1000)
                    player_elo.save()

                if player.wl == "W":
                    w_team_elo += player_elo.elo
                    w_team_nums += 1
                elif player.wl == "L":
                    l_team_elo += player_elo.elo
                    l_team_nums += 1
                
            
            diff = elo_diff(w_team_elo/w_team_nums,l_team_elo/l_team_nums,"W")

            for player in players_list:
                player_elo = CurrentPlayerElo.objects.get(pk = player.player_id)
                if player.wl == "W":
                    player_elo.elo += diff*player_elo.elo/w_team_elo
                elif player.wl == "L":
                    player_elo.elo -= diff*player_elo.elo/l_team_elo
                player_elo.save()
                if today - convert_date(game.game_date) < datetime.timedelta(days=180):
                    HistoricalPlayerElo(elo = player_elo.elo,date = game.game_date, player_id = player_elo.player_id).save()
            if (indx+1)%10000 == 0:
                print(indx + 1)

def run():
    ComputeTeams.write_games()
    ComputeTeams.write_team_elo()
    ComputePlayers.write_player_games()
    ComputePlayers.write_player_elo()
    