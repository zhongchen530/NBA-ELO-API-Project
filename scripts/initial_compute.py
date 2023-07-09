
from NBA.models import *
from nba_api.stats.static import teams,players
from nba_api.stats.endpoints import leaguegamefinder,playergamelogs
from NBA.name_enums import DfColumnNames,TableColumnNames
import datetime
import time
from NBA.nba_api_helper import NBA_ApiHelper
from NBA.reformat import reformat
import pandas as pd
from NBA.name_enums import DfColumnNames,TableColumnNames
import os

def elo_diff(elo1,elo2,wl):
    p1_win = 1/(1+10**((elo2-elo1)/400))
    if wl == "W":
        score = 1
    elif wl == "L":
        score = 0
    elif wl == "T":
        score = 0.5
    else:
        return 0
    return 32*(score - p1_win)

def get_seasons_list():
    return [f"20{str(i).zfill(2)}-{str(i+1).zfill(2)}" for i in range(23)]

def convert_str_to_date(date_str):
    return datetime.datetime.strptime(date_str,'%Y-%m-%d').date()

class ComputeTeams:
    def get_team_games_df(season):
        team_games = leaguegamefinder.LeagueGameFinder(season_nullable=season)
        teams_games_df = team_games.get_data_frames()[0]
        teams_games_df = reformat(teams_games_df,DfColumnNames.TEAM_ID.value)
        return teams_games_df

    def write_games_with_df(df):
        for indx,row in df.iterrows():
            object = Game.objects.create(game_id = row[DfColumnNames.GAME_ID.value],team_id = row[DfColumnNames.TEAM_ID.value + "_x"],game_date = row[DfColumnNames.GAME_DATE.value],opponent_id = row[DfColumnNames.TEAM_ID.value + "_y"])
            object.save()

    def write_team_elo_with_df(df,elo_diff):
        for indx,game in df.iterrows():
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

    def compute_team_elo_from_db(elo_diff):
        sort_by = TableColumnNames.GAME_DATE.value
        games = Game.objects.order_by(sort_by)
        df = pd.DataFrame(games.values())
        ComputeTeams.write_team_elo_with_df(df,elo_diff)
        

class ComputePlayers:
    def write_playergamelogs_with_df(df):
        player_id_name = DfColumnNames.PLAYER_ID.value
        game_id_name = DfColumnNames.GAME_ID.value
        wl_name =  DfColumnNames.WL.value
        
        for indx,game in df.iterrows():
            object = PlayerGame(player_id = game[player_id_name],game_id = game[game_id_name],wl = game[wl_name])
            object.save()

    def get_playergamelogs_df(season):
        col_names = [DfColumnNames.PLAYER_ID.value,DfColumnNames.GAME_ID.value,DfColumnNames.WL.value]
        season_game_logs = playergamelogs.PlayerGameLogs(season_nullable=season)
        df = season_game_logs.get_data_frames()[0]
        df = df[col_names]
        return df

    def compute_player_elo_from_db():
        games = Game.objects.order_by(TableColumnNames.GAME_DATE.value)
        df = pd.DataFrame(games.values())
        ComputePlayers.write_player_elo_with_df(df)

    def write_player_elo_with_df(df):
        today = datetime.date.today()
        df.columns = [col_name.lower() for col_name in df.columns]
        for indx,game in df.iterrows():
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
                if today - convert_str_to_date(game.game_date) < datetime.timedelta(days=180):
                    HistoricalPlayerElo(elo = player_elo.elo,date = game.game_date, player_id = player_elo.player_id).save()

def run():
    if os.environ.get("db_is_empty",False):
        for season in get_seasons_list():
            df = ComputeTeams.get_team_games_df(season)
            ComputeTeams.write_games_with_df(df) 
        ComputeTeams.compute_team_elo_from_db(elo_diff=elo_diff)

        for season in get_seasons_list():
            df = ComputePlayers.get_playergamelogs_df(season)
            ComputePlayers.write_playergamelogs_with_df(df)
        ComputePlayers.compute_player_elo_from_db(elo_diff = elo_diff)
    