from datetime import timedelta

from django.db import models
from django.db.models import Q


class PlayerIndex(models.Model):
    class Meta:
        db_table = 'player_index'

    pid1 = models.IntegerField(default=0)
    pid2 = models.IntegerField(default=0)
    pid3 = models.IntegerField(default=0)
    pid4 = models.IntegerField(default=0)

    empire = models.IntegerField(default=0)

    @property
    def empire_to_name(self):
        if self.empire == 1:
            return "Shinsoo"

        if self.empire == 2:
            return "Chunjo"

        return "Jinno"


class Player(models.Model):
    class Meta:
        db_table = 'player'

    name = models.CharField(max_length=17)
    kills = models.IntegerField(db_column="ludzie")
    job = models.IntegerField(default=0)
    playtime = models.IntegerField(default=0)

    @property
    def place(self):
        return list(
            Player.objects.all().order_by('-kills').values_list('id', flat=True)
        ).index(self.pk) + 1

    @property
    def job_to_class(self):
        if self.job in [0, 4]:
            return "Wojownik"

        if self.job in [1, 5]:
            return "Ninja"

        if self.job in [2, 6]:
            return "Sura"

        if self.job in [3, 7]:
            return "Szaman"

    @property
    def get_empire(self):
        index = PlayerIndex.objects.filter((
            Q(pid1=self.id)
            | Q(pid2=self.id)
            | Q(pid3=self.id)
            | Q(pid4=self.id)
        )).first()

        if index:
            return index.empire_to_name

    @property
    def playtime_label(self):
        hours, minutes = divmod(self.playtime, 60)
        days, hours = divmod(hours, 24)

        hours_string = self._get_hours_string(hours)
        days_string = self._get_days_string(days)

        if days_string and hours_string:
            return f"{days_string}, {hours_string}"

        if days_string and not hours_string:
            return f"{days_string}"

        if not days_string and hours_string:
            return f"{hours_string}"

        return self._get_minutes_string(minutes)

    def _get_hours_string(self, hours):
        if not hours:
            return ""

        if hours == 1:
            return f"{hours} godzina"

        if hours > 1 and hourse < 5:
            return f"{hours} godziny"

        return f"{hours} godzin"

    def _get_days_string(self, days):
        if not days:
            return ""

        if days == 1:
            return f"{days} dzień"

        return f"{days} dni"

    def _get_minutes_string(self, minutes):
        if minutes == 1:
            return f'{minutes} minuta'

        if minutes > 1 and minutes < 5:
            return f'{minutes} minuty'

        return f'{minutes} minut'


class Guild(models.Model):
    class Meta:
        db_table = 'guild'

    name = models.CharField(max_length=12, default='')
    ladder_point = models.IntegerField()

    win = models.IntegerField(default=0)
    draw = models.IntegerField(default=0)
    loss = models.IntegerField(default=0)

    @property
    def place(self):
        return list(
            Guild.objects.all().order_by('-ladder_point').values_list('id', flat=True)
        ).index(self.pk) + 1
