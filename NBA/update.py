from nba_api.stats.endpoints import leaguegamefinder
from datetime import date,timedelta

class Update:
    def update_team_elo():
        today = date.today() - timedelta(days = 30)
        today = today.strftime("%m/%d/%Y")
        return leaguegamefinder.LeagueGameFinder(date_from_nullable=today)