from NBA.initial_compute import get_seasons_list,ComputePlayers,ComputeTeams,elo_diff
from NBA.update import Update

def run():
    for season in get_seasons_list(2020):
        df = ComputeTeams.get_team_games_df(season)
        ComputeTeams.write_games_with_df(df) 
    ComputeTeams.compute_team_elo_from_db(elo_diff=elo_diff)
    print("Team data computed")

    for season in get_seasons_list(2020):
        df = ComputePlayers.get_playergamelogs_df(season)
        ComputePlayers.write_playergamelogs_with_df(df)
    ComputePlayers.compute_player_elo_from_db(elo_diff = elo_diff)
    print("Player data computed")

    Update.update_player_ranking()
    Update.update_team_ranking()
    print("Data is ready!")