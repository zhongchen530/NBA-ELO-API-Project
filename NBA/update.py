from nba_api.stats.endpoints import leaguegamefinder,playergamelogs
from datetime import date,timedelta
from NBA.reformat import reformat
from NBA.models import *
from nba_api.stats.library.parameters import SeasonAll
from NBA.initial_compute import elo_diff,ComputePlayers,ComputeTeams
from .nba_api_helper import PlayerInfo,TeamInfo
import NBA.redis_connection as redis_connection
import json



class Update:
    def get_new_games():
        season = SeasonAll.current_season
        recent_games = leaguegamefinder.LeagueGameFinder(season_nullable=season)
        df = recent_games.get_data_frames()[0]
        df = reformat(df,id_name="TEAM_ID")

        new_indexs = set([indx for indx,row in df.iterrows() if len(Game.objects.filter(game_id = row["GAME_ID"]))==0])
        df = df[df.index.isin(new_indexs)]
        return df
    
    def get_new_playerlogs():
        season = SeasonAll.current_season
        recent_playerlogs = playergamelogs.PlayerGameLogs(season_nullable=season)
        df = recent_playerlogs.get_data_frames()[0]
        
        new_indexs = set([indx for indx,row in df.iterrows() if len(PlayerGame.objects.filter(game_id = row["GAME_ID"]))==0])
        df = df[df.index.isin(new_indexs)]
        return df

    def update_data():
        new_games = Update.get_new_games()
        new_playerlogs = Update.get_new_playerlogs()
        ComputeTeams.write_games_with_df(new_games)
        ComputePlayers.write_playergamelogs_with_df(new_playerlogs)

        ComputePlayers.write_player_elo_with_df(new_games,elo_diff=elo_diff)
        ComputeTeams.write_team_elo_with_df(new_games,elo_diff=elo_diff)

        Update.cache_data()
        Update.update_player_ranking()
        Update.update_team_ranking()
        print("Data updated")

    def cache_data():
        day = date.today() - timedelta(days = 180)
        day = day.strftime("%Y-%m-%d")

        def filter(his_elos):
            for his_elo in his_elos:
                if his_elo.date < day:
                    his_elo.delete()

        filter(HistoricalPlayerElo.objects.all())
        filter(HistoricalTeamElo.objects.all())

    def update_player_ranking():
        elos = CurrentPlayerElo.objects.all()
        PlayerInfo.update()
        player_ranking = []
        for elo in elos:
            if elo.player_id not in PlayerInfo.id_to_info:
                continue
            player_info = PlayerInfo.id_to_info[elo.player_id]
            if player_info["is_active"]:
                args = {}
                args["player_name"] = player_info["full_name"]
                args["elo"] = elo.elo
                #args["team_name"] = player_info["team"]
                args["player_id"] = elo.player_id
                player_ranking.append(args)

        player_ranking.sort(key = lambda x:x["elo"],reverse=True)
        redis_connection.redis_conn.set("player_ranking",json.dumps(player_ranking))
    
    def update_team_ranking():
        elos = CurrentTeamElo.objects.all()
        TeamInfo.update()
        team_ranking = []
        for elo in elos:
            if elo.team_id in TeamInfo.id_to_info:
                print("t")
                team_info = TeamInfo.id_to_info[elo.team_id]
                args = {}
                args["team_name"] = team_info["full_name"]
                args["elo"] = elo.elo
                team_ranking.append(args)
        team_ranking.sort(key = lambda x:x["elo"],reverse=True)
        redis_connection.redis_conn.set("team_ranking",json.dumps(team_ranking))
        
    

    
        


        
