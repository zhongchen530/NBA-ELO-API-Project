from django.contrib import admin
from .models import *
admin.site.register(Game)
admin.site.register(CurrentTeamElo)
admin.site.register(HistoricalTeamElo)
admin.site.register(PlayerGame)
admin.site.register(HistoricalPlayerElo)
admin.site.register(CurrentPlayerElo)