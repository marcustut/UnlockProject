import django
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
import datetime

# Create your models here.
class Ranking(models.Model):
    pass

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

class RulesAndRegulation(models.Model):
    rule = models.TextField(unique=True, default='Insert Rules Here.', editable=True)
    pub_date = models.DateTimeField('Date Added', default=django.utils.timezone.now)
	
    def was_added_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
        
    was_added_recently.admin_order_field = 'pub_date'
    was_added_recently.boolean = True
    was_added_recently.short_description = 'Added recently?'

    def __str__(self):
        return self.rule

class EmergencyContact(models.Model):
    name = models.CharField(max_length=200)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)

    def __str__(self):
        return self.name
