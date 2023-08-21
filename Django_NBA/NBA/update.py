from nba_api.stats.endpoints import leaguegamefinder,playergamelogs
from datetime import date,timedelta
from NBA.reformat import reformat
from NBA.models import *
from nba_api.stats.library.parameters import SeasonAll
from NBA.initial_compute import elo_diff,ComputePlayers,ComputeTeams
from .nba_api_helper import PlayerInfo,TeamInfo
import NBA.redis_connection as redis_connection
import json
from .name_enums import TableColumnNames,DfColumnNames



class Update:
    def get_new_games():
        season = SeasonAll.current_season
        recent_games = leaguegamefinder.LeagueGameFinder(season_nullable=season)
        df = recent_games.get_data_frames()[0]
        df = reformat(df,id_name="TEAM_ID")
    
        old_games = set([game.game_id for game in Game.objects.all()])
        df = df.loc[~df[DfColumnNames.GAME_ID.value].isin(old_games)]
        return df
    
    def get_new_playerlogs():
        season = SeasonAll.current_season
        recent_playerlogs = playergamelogs.PlayerGameLogs(season_nullable=season)
        df = recent_playerlogs.get_data_frames()[0]
        
        old_games = set([game.game_id for game in PlayerGame.objects.all()])
        df = df.loc[~df[DfColumnNames.GAME_ID.value].isin(old_games)]
        return df

    def update_data():
        print("Starting update")
        new_games = Update.get_new_games()
        print("Fetched new games")
        new_playerlogs = Update.get_new_playerlogs()
        print("Fetched playerlogs")
        ComputeTeams.write_games_with_df(new_games)
        print("Wrote games")
        ComputePlayers.write_playergamelogs_with_df(new_playerlogs)
        print("Wrote playerlogs")

        ComputePlayers.write_player_elo_with_df(new_games,elo_diff=elo_diff)
        print("Wrote player elo")
        ComputeTeams.write_team_elo_with_df(new_games,elo_diff=elo_diff)
        print("Wrote team elo")

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
                team_info = TeamInfo.id_to_info[elo.team_id]
                args = {}
                args["team_name"] = team_info["full_name"]
                args["elo"] = elo.elo
                team_ranking.append(args)
        team_ranking.sort(key = lambda x:x["elo"],reverse=True)
        redis_connection.redis_conn.set("team_ranking",json.dumps(team_ranking))
        
    

    
        


        
