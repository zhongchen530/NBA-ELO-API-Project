import pandas as pd
print("dddddddddddddddddddddddddd")
from NBA.models import Game,Current_team_elo,Historical_team_elo
import NBA.getGames

def run():
    print(NBA.getGames.get_player_size())
    return
    Current_team_elo.objects.all().delete()
    Historical_team_elo.objects.all().delete()
