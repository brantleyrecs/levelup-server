from django.db import models
from .gamer import Gamer
from .game_type import GameType

class Game(models.Model):
  title = models.CharField(max_length=55)
  game_type = models.ForeignKey(GameType, on_delete=models.CASCADE)
  maker = models.CharField(max_length=55)
  gamer = models.ForeignKey(Gamer, on_delete=models.CASCADE)
  number_of_players = models.IntegerField()
  skill_level = models.IntegerField()
