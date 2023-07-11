from django.test import TestCase, Client
import NBA.initial_compute as initial_compute
from NBA.models import *
import pandas as pd
from NBA.name_enums import DfColumnNames,TableColumnNames

class TestCompute(TestCase):
    def test_get_and_write_teams_games(self):
        col_names = [DfColumnNames.GAME_DATE.value,DfColumnNames.GAME_ID.value,DfColumnNames.WL.value, DfColumnNames.TEAM_ID.value + "_x", DfColumnNames.TEAM_ID.value + "_y"]
        season = "2020-21"
        df = initial_compute.ComputeTeams.get_team_games_df(season)
        print(df.columns)
        print([col_name in df.columns for col_name in col_names])
        self.assertTrue(all(col_name in df.columns for col_name in col_names))
        self.assertTrue(df[DfColumnNames.GAME_ID.value].nunique() == len(df))
        initial_compute.ComputeTeams.write_games_with_df(df)
    
    def test_teams_elo_compute(self):
        Game(game_id = 0,team_id = 0,game_date = "2020-01-01",wl = "W",opponent_id = 1).save()
        Game(game_id = 1,team_id = 0,game_date = "2020-01-02",wl = "W",opponent_id = 2).save()
        Game(game_id = 2,team_id = 1,game_date = "2020-01-03",wl = "W",opponent_id = 2).save()

        def elo_diff(t1,t2,wl):
            if wl == "W":
                return 1
            elif wl == "L":
                return -1
            elif wl == "T":
                return 0

        initial_compute.ComputeTeams.compute_team_elo_from_db(elo_diff)

        t0 = CurrentTeamElo.objects.get(pk = 0) 
        t1 = CurrentTeamElo.objects.get(pk = 1)
        t2 = CurrentTeamElo.objects.get(pk = 2)
        print(t0,t1,t2)
        self.assertTrue(t0.elo > t1.elo > t2.elo)
        self.assertTrue(t0.elo == 1002)
        self.assertTrue(t1.elo == 1000)
        self.assertTrue(t2.elo == 998)
    
    def test_write_gameslogs(self):
        season = "2020-21"
        df = initial_compute.ComputePlayers.get_playergamelogs_df(season)
        initial_compute.ComputePlayers.write_playergamelogs_with_df(df)
        
        query = pd.DataFrame(PlayerGame.objects.all().values())
        query.drop(["id"],axis = 1,inplace=True)
        
        df = df.astype({DfColumnNames.GAME_ID.value:int})
        #query = query.astype({colname:str for colname in query.columns})
        #df = df.astype({colname:str for colname in df.columns})

        df.columns = [cname.lower() for cname in df.columns]
        
        self.assertTrue(query.equals(df))
    
