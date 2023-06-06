from django.db import models

class Game(models.Model):
    game_id = models.IntegerField(primary_key = True)
    team_id = models.IntegerField()
    game_date = models.CharField(max_length=15)
    wl = models.CharField(max_length=1)
    opponent_id = models.IntegerField()

    def __str__(self):
        return str(self.game_id) + " " + self.game_date

class Historical_team_elo(models.Model):
    team_id = models.IntegerField()
    date = models.CharField(max_length=15)
    elo = models.FloatField()

    class Meta:
        indexes = [models.Index(fields=["team_id","date"]),]

    def __str__(self):
        return str(self.team_id) + " " + self.date + " " + str(self.elo)

class Current_team_elo(models.Model):
    team_id = models.IntegerField(primary_key = True)
    elo = models.FloatField()

    def __str__(self):
        return str(self.team_id) + " " + str(self.elo)



