from django.db import models
from django.utils import timezone
import datetime

# Create your models here.

class Control(models.Model):
    game_time = models.DateTimeField('Game Time')
    ranking_switcher = models.BooleanField(verbose_name='ranking turn on/off', default=False)

    def is_game_time_now(self):
        now = timezone.now()
        return now == self.game_time

    is_game_time_now.admin_order_field = 'game_time'
    is_game_time_now.boolean = True
    is_game_time_now.short_description = 'Is Game Time true?'
