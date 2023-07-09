from nba_api.stats.endpoints import leaguegamefinder,playergamelogs
from datetime import date,timedelta
from NBA.reformat import reformat
from NBA.models import *
from nba_api.stats.library.parameters import SeasonAll
from scripts.initial_compute import elo_diff,ComputePlayers,ComputeTeams


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
        print("updated....")
        return
        new_games = Update.get_new_games()
        new_playerlogs = Update.get_new_playerlogs()
        ComputeTeams.write_games_with_df(new_games)
        ComputePlayers.write_playergamelogs_with_df(new_playerlogs)

        ComputePlayers.write_player_elo_with_df(new_games)
        ComputeTeams.write_team_elo_with_df(new_games)

        Update.cache_data()

    def update_playerlogs_data():
        df = Update.get_new_playerlogs()
        Update.update_player_elo_with_games

    def cache_data():
        day = date.today() - timedelta(days = 180)
        day = day.strftime("%Y-%m-%d")

        HistoricalPlayerElo.objects.filter(date < day).delete()
        HistoricalTeamElo.objects.filter(date < day).delete()





        
