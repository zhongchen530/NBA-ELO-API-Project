from typing import Any, Dict
from django.views.generic.list import ListView
import NBA.redis_connection as redis_connection
import json
import NBA.redis_connection as redis_connection

class TeamRankingView(ListView):
    template_name = "team-ranking.html"
    def get_queryset(self):
        return json.loads(redis_connection.redis_conn.get("team_ranking"))

class PlayerRankingView(ListView):
    template_name = "player-ranking.html"
    def get_queryset(self):
        return json.loads(redis_connection.redis_conn.get("player_ranking"))