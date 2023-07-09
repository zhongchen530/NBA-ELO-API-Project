from NBA.models import *
from nba_api.stats.static import teams,players
from nba_api.stats.endpoints import leaguegamefinder,playergamelog,playergamelogs
import pandas as pd
""" from nba_api.stats.library.parameters import SeasonAll
import time
import pandas as pd
from NBA.update import Update
from nba_api.stats.library.parameters import SeasonAll
from NBA.nba_api_helper import NBA_ApiHelper
from . import initial_compute
 """
from NBA.name_enums import DfColumnNames,TableColumnNames
from nba_api.stats.endpoints import playergamelogs
from NBA.nba_api_helper import NBA_ApiHelper
from nba_api.stats.static import teams
def run():
   #print([ team["name"] for team in teams.get_teams() if team["id"] == 1612709902])
   #print(NBA_ApiHelper.get_team_name(1612709888))
   print(len(teams.get_teams()))

