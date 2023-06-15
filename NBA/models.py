from django.db import models

class Game(models.Model):
    game_id = models.IntegerField(primary_key = True)
    team_id = models.IntegerField()
    game_date = models.CharField(max_length=15)
    wl = models.CharField(max_length=1)
    opponent_id = models.IntegerField()

    def __str__(self):
        return str(self.game_id) + " " + self.game_date

class HistoricalTeamElo(models.Model):
    team_id = models.IntegerField()
    date = models.CharField(max_length=15)
    elo = models.FloatField()

    class Meta:
        indexes = [models.Index(fields=["team_id","date"]),]

    def __str__(self):
        return str(self.team_id) + " " + self.date + " " + str(self.elo)

class CurrentTeamElo(models.Model):
    team_id = models.IntegerField(primary_key = True)
    elo = models.FloatField()

    def __str__(self):
        return str(self.team_id) + " " + str(self.elo)

class PlayerGame(models.Model):
    player_id = models.IntegerField()
    game_id = models.IntegerField()
    wl = wl = models.CharField(max_length=1)

    class Meta:
        indexes = [models.Index(fields=["game_id","wl"]),]

    def str(self):
        return str(self.player_id) + str(self.game_id) + self.wl
    
class CurrentPlayerElo(models.Model):
    player_id = models.IntegerField(primary_key = True)
    elo = models.FloatField()

    def __str__(self):
        return str(self.player_id) + " " + str(self.elo)

class HistoricalPlayerElo(models.Model):
    player_id = models.IntegerField()
    date = models.CharField(max_length=15)
    elo = models.FloatField()

    class Meta:
        indexes = [models.Index(fields=["player_id","date"]),]

    def __str__(self):
        return str(self.player_id) + " " + self.date + " " + str(self.elo)
