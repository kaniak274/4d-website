from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=200)
    kills = models.IntegerField()


class Guild(models.Model):
    guild_name = models.CharField(max_length=200)
    points = models.IntegerField()
