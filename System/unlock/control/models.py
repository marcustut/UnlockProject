from django.db import models
from django.utils import timezone
import datetime

# Create your models here.

class Control(models.Model):
    game_time = models.DateTimeField('Game Time')

    def is_game_time_now(self):
        now = timezone.now()
        return now == self.game_time

    is_game_time_now.admin_order_field = 'game_time'
    is_game_time_now.boolean = True
    is_game_time_now.short_description = 'Is Game Time true?'
