#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 10:24:54 2023

@author: zhongyuanchen
"""
from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder
import pandas as pd

columns = ['SEASON_ID', 'TEAM_ID', 'TEAM_ABBREVIATION', 'TEAM_NAME', 'GAME_ID',
       'GAME_DATE', 'MATCHUP', 'WL']

def get_range(date_range):
    if len(date_range) != 2:
        raise Exception("Expected date_range with length 2,%s given"%len(date_range))
        
    start,end = date_range
    teams_df = []
    for team in teams.get_teams():
        team_id = team["id"]
        team_games = leaguegamefinder.LeagueGameFinder(team_id_nullable = team_id)
        team_df = team_games.get_data_frames()[0]
        team_df = team_df[columns]
        filt = (start <= team_df["GAME_DATE"]) & (team_df["GAME_DATE"] < end)
        team_df = team_df[filt]
        teams_df.append(team_df)

    teams_df = pd.concat(teams_df,axis = 0)
    teams_df.drop_duplicates(subset = "GAME_ID",inplace = True)
    return teams_df
    