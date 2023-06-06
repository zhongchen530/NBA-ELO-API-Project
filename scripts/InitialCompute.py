from NBA import getGames
from NBA.models import Game,Historical_team_elo,Current_team_elo
import os

def write_games():
    date_range = ["2000-00-00","9999-99-99"]
    teams_df = getGames.get_team_games(date_range)
    print(teams_df)
    for indx,row in teams_df.iterrows():
        object = Game(*(row.tolist()))
        object.save()

def elo_diff(elo1,elo2,wl):
    p1_win = 1/(1+10**((elo2-elo1)/400))
    if wl == "W":
        score = 1
    elif wl == "L":
        score = 0
    elif wl == "T":
        score = 0.5

    return 32*(score - p1_win)

def write_elo():
    games = Game.objects.order_by("-game_date")
    for indx,game in enumerate(games):
        try: 
            team1 = Current_team_elo.objects.get(pk = game.team_id)
        except:
            team1 = Current_team_elo(game.team_id,1000)

        try:
            team2 = Current_team_elo.objects.get(pk = game.opponent_id)
        except:
            team2 = Current_team_elo(game.opponent_id,1000)

        diff = elo_diff(team1.elo,team2.elo,game.wl)
        team1.elo += diff
        team2.elo -= diff

        team1.save()
        team2.save()

        helo1 = Historical_team_elo(indx,team1.team_id,game.game_date,team1.elo)
        helo2 = Historical_team_elo(indx,team2.team_id,game.game_date,team2.elo)

        helo1.save()
        helo2.save()

def run():
    write_elo()
