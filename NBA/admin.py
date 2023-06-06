from django.contrib import admin
from .models import Game,Current_team_elo,Historical_team_elo
admin.site.register(Game)
admin.site.register(Current_team_elo)
admin.site.register(Historical_team_elo)
