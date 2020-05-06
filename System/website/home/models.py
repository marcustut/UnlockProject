from django.db import models
from django import forms
from django.utils import timezone
import datetime
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class MissionDetail(models.Model):
    mission_title = models.CharField(max_length=200, default="Insert Mission Title Here.")
    mission_description = models.CharField(max_length=200, default="Insert Mission Details Here.")
    start_time = models.DateTimeField('Start Time')
    end_time = models.DateTimeField('End Time')

    def check_date(self, year, month, day):
        start_time = datetime.datetime(year, month, day, 0, 0, tzinfo=None)
        end_time = datetime.datetime(year, month, day, 23, 59, tzinfo=None)
        return start_time <= self.start_time.replace(tzinfo=None) <= end_time

    def nearest_mission(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.start_time <= now

    nearest_mission.admin_order_field = 'start_time'
    nearest_mission.boolean = True
    nearest_mission.short_description = 'Today\'s Mission'

    def __str__(self):
        return self.mission_title

class AccountDetail(models.Model):
    name = models.CharField(max_length=200)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    satellite = models.CharField(max_length=200)
    pastoral_team = models.CharField(max_length=200)
    pastoral_cg = models.CharField(max_length=200)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=128)
    points = models.IntegerField(default=0)
