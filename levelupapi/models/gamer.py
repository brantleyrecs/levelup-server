from django.db import models

class Gamer(models.Model):
  bio = models.CharField(max_length=55)
  uid = models.IntegerField()
