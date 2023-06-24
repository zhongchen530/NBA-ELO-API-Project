from django.test import TestCase, Client
import NBA.update as update
from scripts.initial_compute import elo_diff,ComputePlayers,ComputeTeams
from nba_api.stats.library.parameters import SeasonAll
from NBA.models import *
import pandas as pd
from NBA.name_enums import DfColumnNames,TableColumnNames

class TestUpdate(TestCase):
    def test_get_new_games(self):
        games = update.Update.get_new_games()
        ComputeTeams.write_games_with_df(games.iloc[:10])
        new_games = update.Update.get_new_games()
        self.assertTrue(len(games)- 10 == len(new_games))
        concat_df = pd.concat([new_games,games.iloc[:10]],axis = 0)
        concat_df.sort_values("GAME_ID",inplace=True)
        games.sort_values("GAME_ID",inplace=True)
        self.assertTrue(concat_df.equals(games))

    def test_get_new_playerlogs(self):
        playerlogs = update.Update.get_new_playerlogs()
        filt = playerlogs[DfColumnNames.GAME_ID.value] == playerlogs.iloc[0][DfColumnNames.GAME_ID.value]
        sub_playerlogs = playerlogs[filt]

        ComputePlayers.write_playergamelogs_with_df(sub_playerlogs)
        new_playerlogs = update.Update.get_new_playerlogs()
        self.assertTrue(len(playerlogs) - len(sub_playerlogs) == len(new_playerlogs))

        concat_df = pd.concat([sub_playerlogs,new_playerlogs])
        concat_df.sort_index(inplace=True)
        playerlogs.sort_index(inplace=True)
        print(concat_df)
        print(playerlogs)
        self.assertTrue(concat_df.equals(playerlogs))


